import requests
import re
from datetime import datetime, date

import bs4


class TransportLineError(Exception):
    """Raised for all expected and recoverable errors in TransportLine class"""


class TransportLine(object):
    """ Class for scraping bus stop times from IDOS.
        @param init_stop ... First stop name
        @param exit_stop ... Last stop name
        @param n_results ... number of the earliest bus connections to be
                             written out [default: 3]

        Basic usage: to get the next 3 bus connections from foo to baz use
        TransportLine("foo", "baz").get_times()
    """

    # regexp to get div containing the bus connection details
    regexp = re.compile('connectionBox.+')

    def __init__(self, init_stop, exit_stop, n_results=3):
        self.init_stop = init_stop
        self.exit_stop = exit_stop
        self.n_results = n_results


    def get_times(self):
        """ Returns the n_results first bus connections departing separated by
            newline.
        """
        results = [f"Line           |    Time    |  Δ(min)"]
        url = self._get_url()
        text = self._get_page(url)
        soup = bs4.BeautifulSoup(text)

        connection_boxes = soup.find_all('div', id=self.regexp)

        if len(connection_boxes) < self.n_results:
            # FIXME: handle this in some other way?
            raise TransportLineError(f"Error: There are {len(connection_boxes)}"\
                                     f"found and we want to get at least {self.n_results}")

        for connection in connection_boxes[:self.n_results]:
            print(connection, "\n \n\n")
            results.append(self._parse_times(connection))

        return "\n".join(results)


    def _get_url(self):
        """ Returns the URL of the IDOS page with search results for the earliest
            connections from first stop to last stop.
        """
        # the tc and fc vars define the transport providers that are searched
        # for the publ. transport stops. E.g. 301003 ~ PID
        return 'https://idos.idnes.cz/vlakyautobusymhdvse/spojeni/vysledky/'\
                f'?f={self.init_stop}&fc=301003&t={self.exit_stop}&tc=301003'


    def _get_page(self, url):
        """ Get the html page from url. Raises TransportLineError on fail."""
        try:
            result = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise TransportLineError('Could not reach the server.')

        if result.status_code == 200:
            return result.text
        else:
            raise TransportLineError(
                  'Error http request returned error {result.status_code}')


    def _parse_times(self, connection):
        time_div = connection.find_all(attrs={'class': "reset stations first last"})
        line_name = connection.find_all(
            title = [re.compile('metro.+'), re.compile('tramvaj.+'), re.compile('autobus.+')])[0].text
        arrival_time = time_div[0].find(self._is_first_station_time)
        print(arrival_time)
        arrival_time = time_div[0].find(self._is_first_station_time).text
        print(arrival_time)


        # get the time delta from now
        try:
            time = datetime.fromisoformat(date.today().isoformat() + 'T' + arrival_time)
            tim_delta = (time - datetime.now()).total_seconds()//60
            if tim_delta < 0:
                tim_delta = 0
        except:
            #tim_delta = 'NaN'
            tim_delta = 0


        return f"{line_name:<7}    |    {arrival_time}   |   {int(tim_delta):>4d}"
        return [line_name, arrival_time, tim_delta]


    def _is_last_station_time(self, tag):
        return tag.attrs.get('class') == ['reset', 'time'] and\
               self.exit_stop in tag.next_sibling.text


    def _is_first_station_time(self, tag):
        return all(x in tag.attrs.get('class') for x in ['reset', 'time'])   and\
               self.init_stop in tag.next_sibling.text

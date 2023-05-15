#!/usr/bin/env python3
"""Simple pagination."""


import csv
from math import ceil
from typing import List, Tuple, Dict


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialise the class."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cache dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Do pagination."""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        cor_range: Tuple = index_range(page, page_size)
        data: List = self.dataset()

        return (data[cor_range[0]: cor_range[1]])

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return dict."""
        data = []
        try:
            data = self.get_page(page, page_size)
        except AssertionError:
            return {}

        dataset: List = self.dataset()
        totalpage: int = len(dataset) if dataset else 0
        totalpage = ceil(totalpage / page_size)
        prevpage: int = (page - 1) if (page - 1) >= 1 else None
        nextpage: int = (page + 1) if (page + 1) <= totalpage else None

        return ({
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': nextpage,
            'prev_page': prevpage,
            'total_pages': totalpage,
        })


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Description.

    -------------
    Return a tuple of size two containing a start index and an
    end index corresponding to the range of indexes to return in a
    list for those particular pagination parameters.
    """
    end: int = page * page_size
    start: int = end - page_size
    return (start, end)

from Pages.search_page import SearchPage
import config
from TestData import search_filters


def test_1_search_by_brand(test_driver, test_logger):

    search = SearchPage(test_driver, test_logger)
    search.go_to_page(config.home_url)

    # search classic sunglassis
    search.search_data(search_filters.search_data)
    assert 1 == 2
    # # Filter data and return how many items are 
    # search.filter_data_by_brand_price_color(search_filters.brand_name, search_filters.price_range, search_filters.color)
    # result_count = search.get_result_count()
    # test_logger.info(f"{result_count} items found.")
    
    # # Check that informtaion of search data is correct
    # assert search.check_selected_price(search_filters.price_range)
    # assert search.check_selected_brand(search_filters.brand_name)





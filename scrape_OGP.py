import os
import time
from os import path
import pandas as pd
import asyncio

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


basedir = path.abspath(path.dirname(__file__))
OGP_DATA_FILEPATH = os.path.join(basedir, "OGP", "OGP Output.xlsx")
# OGP_URL = "https://beta.data.gov.sg/collections?sort=Last%20updated"
OGP_URL = 'https://beta.data.gov.sg/datasets'

def transform_data_output():
    # Read data from Excel file
    df = pd.read_excel(OGP_DATA_FILEPATH)

    given_data = df['Source Info'].tolist()

    # Splitting the given data into individual components
    period = []
    num_datasets = []
    file_types = []
    company_columns = []

    for item in given_data:
        components = item.split("•")
        if len(components) == 3:
            # Case where datasets are appended to period
            period.append(None)
            num_datasets.append(components[0])
            file_types.append(components[1])
            company_columns.append(components[2])
        else:
            period.append(components[0])
            num_datasets.append(components[1])
            file_types.append(components[2])
            company_columns.append(components[3])

    # Creating a DataFrame from given data
    given_df = pd.DataFrame({
        'Period': period,
        'No. of Datasets': num_datasets,
        'File Types Available': file_types,
        'Company': company_columns
    })

    # Concatenate new DataFrame with original DataFrame after dropping 'source info' column
    merged_df = pd.concat([df.drop(columns=['Source Info']), given_df], axis=1)

    return merged_df


async def count_p_occurrences(page, xpath):
    try:
        # Select all elements matching the XPath
        elements = await page.query_selector_all(xpath)

        # Filter out only the <p> elements
        p_elements = [element for element in elements if
                      await element.evaluate('(el) => el.tagName.toLowerCase()') == 'p']

        return len(p_elements)

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


async def count_occurrences(page, xpath):
    elements = await page.query_selector_all(xpath)
    return len(elements)


def remove_excel_content(excel_filepath):
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_filepath, header=None)

    # Create an empty DataFrame with the same columns
    df_empty = pd.DataFrame(columns=df.columns)

    # Save the empty DataFrame to the Excel file, effectively removing its contents
    df_empty.to_excel(excel_filepath, index=False, header=False)


# def output_to_excel(title, source, period, dataset_number, file_type, gov_agency):
def output_to_excel(title, source, source_info):
    df = pd.read_excel(OGP_DATA_FILEPATH)
    # Create a dictionary using the function parameters
    my_dict = {
        'Title': title,
        'Source': source,
        'Source Info': source_info
    }

    # Convert the dictionary to a DataFrame and concatenate it with the original DataFrame
    df_dict = pd.DataFrame([my_dict])
    df = pd.concat([df, df_dict], ignore_index=True)

    # Save df to Excel
    df.to_excel(OGP_DATA_FILEPATH, index=False)

    # # Print the resulting DataFrame
    # print("DataFrame after appending the row:")
    # print(df)


async def scrape_export(page, start_count, end_count):
    for i in range(start_count, end_count + 1):
        # title
        TITLE_XPATH = f'((//*[@class="chakra-link css-mfiv8d"])[{i}]//p[1])[1]'
        title_element = await page.wait_for_selector(TITLE_XPATH)
        if title_element:
            title = await title_element.inner_text()
            # print(title)

        # source
        SOURCE_XPATH = f'((//*[@class="chakra-link css-mfiv8d"])[{i}]//p[1])[2]'
        source_element = await page.wait_for_selector(SOURCE_XPATH)
        if source_element:
            source = await source_element.inner_text()
            # print(source)

        # source info
        SOURCEINFO_XPATH = f'(//*[@class="chakra-link css-mfiv8d"]//ul)[{i}]'
        sourceinfo_element = await page.wait_for_selector(SOURCEINFO_XPATH)
        if sourceinfo_element:
            source_info = await sourceinfo_element.inner_text()
            source_info = source_info.replace('\n', '')
            # print(source_info)

        # Export to excel
        output_to_excel(title, source, source_info)


async def scrape_ogp():
    retry_counter = 0
    while retry_counter < 3:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            browser_context = await browser.new_context()
            page = await browser_context.new_page()
            await page.goto(OGP_URL)

            # Clean Excel File content
            remove_excel_content(OGP_DATA_FILEPATH)
            print("Excel content cleared")

            # Read the collection number to do loop
            time.sleep(3)
            element = await page.wait_for_selector('//p[@class="chakra-text css-19ryvij"]')
            text_content = await element.inner_text()
            text_content_without_comma = text_content.replace(",", "")
            integer_value = int(text_content_without_comma)
            print(integer_value)

            # Click till load button does not exists
            LOAD_BTN_XPATH = '//button[text()="Load more"]'
            click_count = 0
            start_count = 1
            while True:
                try:
                    # Wait for load button xpath to appear
                    LOAD_BTN = await page.wait_for_selector(LOAD_BTN_XPATH)

                    # Count xpath occurence
                    OCCURENCE_XPATH = '//*[@class="chakra-link css-mfiv8d"]'
                    end_count = await count_occurrences(page, OCCURENCE_XPATH)
                    print(f"End Count: {end_count}")

                    await scrape_export(page, start_count, end_count)
                    start_count += 20
                    print(start_count)
                    print(f"Start Count: {start_count}")

                    await LOAD_BTN.click()
                    click_count += 1
                    print(f"Clicked on 'Load more' button {click_count} time(s)")

                except PlaywrightTimeoutError as e:
                    print(f"An error occurred, button can't be found: {e}")
                    print("No more 'Load more' button found")
                    print(f"Load more button has been clicked {click_count} times")

                    # Count xpath occurence
                    OCCURENCE_XPATH = '//*[@class="chakra-link css-mfiv8d"]'
                    end_count = await count_occurrences(page, OCCURENCE_XPATH)
                    print(f"End Count: {end_count}")

                    # Export
                    await scrape_export(page, start_count, end_count)

                    # Transform and Save
                    merged_df = transform_data_output()
                    merged_df.to_excel(OGP_DATA_FILEPATH, index=False)

                    break

            break

    if retry_counter == 3:
        print('Fail')
    else:
        print('Success')

asyncio.run(scrape_ogp())


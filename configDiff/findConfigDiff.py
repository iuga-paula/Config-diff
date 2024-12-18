import os
import hashlib
import sys
import argparse

ignored_files = ['copernicus.settings', 'matomo.settings',
                 'system.site',
                 'views.view.content_listings',
                 'views.view.search',
                 'webform.webform.contact',
                 'block.block',
                 'blazy.settings.yml',
                 'core.entity_form_display.node.homepage.default.yml',
                 'core.entity_form_display.node.page.default.yml',
                 'core.entity_form_display.node.provider.default.yml',
                 'core.entity_form_display.taxonomy_term.countries.default.yml',
                 'core.entity_form_display.taxonomy_term.keywords.default.yml',
                 'core.entity_view_display.block_content.block_text_with_image.default.yml',
                 'core.entity_view_display.media.video.default.yml',
                 'core.entity_view_display.media.video.preview.yml',
                 'core.entity_view_display.menu_link_content.main.menu_link_with_image.yml',
                 'core.entity_view_display.node.event.default.yml',
                 'core.entity_view_display.node.event.search_result.yml',
                 'core.entity_view_display.node.event.teaser.yml',
                 'core.entity_view_display.node.homepage.default.yml',
                 'core.entity_view_display.node.homepage.full.yml',
                 'core.entity_view_display.node.homepage.teaser.yml',
                 'core.entity_view_display.node.page.carousel_teaser.yml',
                 'core.entity_view_display.node.page.custom_page_teaser.yml',
                 'core.entity_view_display.node.page.default.yml',
                 'core.entity_view_display.node.page.featured.yml',
                 'core.entity_view_display.node.page.featured_homepage.yml',
                 'core.entity_view_display.node.page.full.yml',
                 'core.entity_view_display.node.page.provider.yml',
                 'core.entity_view_display.node.page.search_result.yml',
                 'core.entity_view_display.node.page.sidebar_teaser.yml',
                 'core.entity_view_display.node.page.teaser.yml',
                 'core.entity_view_display.node.page.teaser_without_date.yml',
                 'core.entity_view_display.node.page.teaser_without_image.yml',
                 'core.entity_view_display.node.page.tender_teaser.yml',
                 'core.entity_view_display.node.page.two_column_list.yml',
                 'core.entity_view_display.node.provider.custom_page_teaser.yml',
                 'core.entity_view_display.node.provider.default.yml',
                 'core.entity_view_display.node.provider.teaser.yml',
                 'core.entity_view_display.paragraph.card.default.yml',
                 'core.entity_view_display.paragraph.image_caption_download_dropdown.featured.yml',
                 'core.entity_view_display.paragraph.image_caption_download_dropdown.preview.yml',
                 'core.entity_view_display.paragraph.image_caption_download_dropdown.preview_square_thumbnail.yml',
                 'core.entity_view_display.paragraph.large_text_and_image.default.yml',
                 'core.entity_view_display.paragraph.list_items.default.yml',
                 'core.entity_view_display.paragraph.paragraph_with_image.default.yml',
                 'core.entity_view_display.paragraph.section_title.default.yml',
                 'core.entity_view_display.taxonomy_term.help_and_support.token.yml',
                 'core.entity_view_display.taxonomy_term.help_and_support.default.yml',
                 'core.entity_view_display.taxonomy_term.page_function.default.yml',
                 'filter.format.basic_html.yml',
                 'filter.format.plain_text.yml',
                 'filter.format.restricted_html.yml',
                 'google_analytics.settings.yml',
                 'gtm.settings.yml',
                 'image.style.media_crop_preview.yml',
                 'pathauto.pattern.default.yml',
                 'responsive_image.styles.featured_image.yml',
                 'responsive_image.styles.slideshow.yml',
                 'responsive_image.styles.teaser.yml',
                 'role_hierarchy.settings.yml',
                 'scheduler.settings.yml',
                 'views.view.authors.yml',
                 'views.view.content.yml',
                 'views.view.content_selectors.yml',
                 'views.view.copernicus_terms.yml',
                 'views.view.media_listings.yml',
                 'views.view.news_landing_page.yml',
                 'views.view.votingapi_votes.yml',
                 'xmlsitemap.settings.node.event.yml',
                 'xmlsitemap.xmlsitemap.g3XYqcXbSKPVBDODwnT6pq7oqhCFkPryj4vVqrl_Kfc.yml',
                 'system.mail.yml',
                 'smtp.settings.yml']


def calculate_hash(file_path, remove_uuids):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Skip uuids and config hashes
                if remove_uuids and (
                        line.strip().startswith("uuid:") or line.strip().startswith("default_config_hash:")
                ):
                    continue
                # Update the hash with the remaining content
                hasher.update(line.encode('utf-8'))
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def compareFiles(source_dir, destination_dir, remove_uuids):
    notFoundTxt = open("../results/not_found_files.txt", "w")
    differentFilesTxt = open("../results/different_content.txt", "w")
    file_map = {}

    # Map source files
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.startswith(tuple(ignored_files)):
                continue
            file_path = os.path.join(root, file)
            file_map[file_path] = calculate_hash(file_path, remove_uuids)

    # Check differences
    sorted_items = sorted(file_map.items())
    for file_path, file_hash in sorted_items:
        destination_file_path = file_path.replace(source_dir, destination_dir)
        configName = destination_file_path.replace(destination_dir, '')
        configName = configName.lstrip('/')
        if not os.path.isfile(destination_file_path):
            notFoundTxt.write(configName + "\n")
            print("Config not found in destination path: " + configName)
            continue
        if file_hash != calculate_hash(destination_file_path, remove_uuids):
            differentFilesTxt.write(configName + "\n")
            print("Different config files for the same file: " + configName)

    notFoundTxt.close()
    differentFilesTxt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=str, help="The source directory to scan.")
    parser.add_argument("config_dir", type=str, help="The configuration directory to scan.")
    parser.add_argument("--removeUUIDs", action="store_true", help="Remove uuids when looking for config diff")
    args = parser.parse_args()

    source = args.source_dir
    destination = args.config_dir
    if not os.path.isdir(source):
        print(f"Source {source} is not a directory!")
        sys.exit(2)
    if not os.path.isdir(destination):
        print(f"Destination {destination} is not a directory!")
        sys.exit(2)

    compareFiles(source, destination, args.removeUUIDs)


if __name__ == "__main__":
    main()
import os
import re
import networkx as nx
from itertools import combinations

def build_temporal_graphs(main_data_folder):
    """
    فایل‌های متنی را می‌خواند و گراف‌های زمانی و تجمعی را می‌سازد.
    """
    all_years = range(1992, 2004)
    edges_by_year = {year: [] for year in all_years}

    for year in all_years:
        folder_path = os.path.join(main_data_folder, str(year))
        if not os.path.exists(folder_path):
            continue
        for filename in os.listdir(folder_path):
            if filename.endswith('.abs'):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    authors_match = re.search(r'Authors:(.+?)\\', content, re.DOTALL)
                    if authors_match:
                        authors_text = authors_match.group(1).strip().replace('\n', ' ').replace(' and ', ',')
                        authors = [author.strip() for author in authors_text.split(',') if author.strip()]
                        if len(authors) > 1:
                            edges_by_year[year].extend(list(combinations(authors, 2)))

    temporal_graphs = {}
    current_graph = nx.Graph()
    for year in sorted(edges_by_year.keys()):
        current_graph.add_edges_from(edges_by_year[year])
        temporal_graphs[year] = current_graph.copy()

    return temporal_graphs, temporal_graphs[2003] # بازگرداندن دیکشنری گراف‌های زمانی و گراف نهایی
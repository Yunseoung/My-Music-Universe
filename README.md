# My-Music-Universe
A fast Python script to parse YouTube view history HTML and export listening data into a network graph format

YouTube Music History Visualizer Data Extractor

A high-performance Python script designed to extract music listening history from Google Takeout's YouTube view history (.html) file and structure it for network graph visualizations. Using regex-based parsing instead of heavy DOM parsers, it quickly filters music records, cleans artist metadata, and outputs a ready-to-use JavaScript data file (universe_data.js) structured into node-link relationships (ME ➔ Artist ➔ Song).

## Features
- **Fast HTML Parsing**: Uses regex pattern matching for lightweight and high-speed processing of large history files.
- **Smart Music Filtering**: Automatically identifies music tracks based on YouTube Music URLs and channel topic identifiers.
- **Visualization-Ready**: Generates structured node-link data (`universe_data.js`) optimized for D3.js and force-directed graph libraries.

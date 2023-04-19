
- Gathers the wiki pages from the database dump
- Extracts relevant pages
- Inspects sections for links (currently manual, see old commit for other)
  - using marko: markdown parsing
  - wikimarkup: converts to HTML, uses beautifulsoup to extract texts
  - manual: rough (but fast and robust) text processing
- Postprocesses links
- Caches information
- Generates interactive graph using pyvis network

## Reference

- https://backrooms.fandom.com/wiki/Special:Statistics
- https://backrooms-freewriting.fandom.com/wiki/Special:Statistics

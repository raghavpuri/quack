# Analyze
# 
# We have at this point crawled data sources and are now importing data structures that have downloadable 
# file links to form our search index
#
# Now for each file we must 
#   Get a file --> Store in Redis --> Analyze semantic idea vectors --> Put these into indexer
SAMPLE_DOWNLOAD_LINK = "https://canvas.brown.edu/files/69501922/download?download_frd=1&verifier=yqXTgytuiCZtKiFYu3nd3Y9BZxf15TlgDrkSP16f"
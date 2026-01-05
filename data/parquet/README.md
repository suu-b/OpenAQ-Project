# Parquet
[Parquet](https://parquet.apache.org/) is a free and open-source column-oriented file data storage format. It is optimized for big data analytics. Unlike CSV-files, it stores data column-wise.

Reference: [Data Mozart](https://youtu.be/5NA57Pfpdr4)

### Notes
Earlier, the only way for MNCs to go was Relational Data. With the rise of unstructured data, certain requirements rose:
1. Organizations want to do data analysis on the data unstructured data. For instance, sentiment analysis on social media content. However, relational databases are not feasible to store unstructured data.
2. Yet organizations wanted to stick to the traditional way but without designing ETL workloads to load these data to warehouses.

### Why Parquet?
1. Data Compression: Parquet file compresses data with various encoding and compression algorithms.
2. Columnar Storage: Faster read and analytical operations.
3. Language Agnostic
4. Open-source format: Not stuck with just one vendor.
5. Support for complex data types.

### Row-based vs Column-based storage
In traditional storage, data is stored as a row: product,customer,country,date,sales
Now, if a query demands 'How many users from the USA bought T-Shirt?'. A row-based storage would scan the whole data from left-to-right. Essentially however, only two columns are required for the answer: product and country.
A columnar storage opts a different path. It physically separates each column from the others. The engine will only scan the necessary ones. This improves the performance.

Parquet, on top of it, **is a columnar format that stores the data in row groups**. 
Columns are still different, but it introduces row-groups that can be wholly skipped on the basis of the predicate of the query. For instance, where product = 'T-Shirt'. Row-groups with no t-shirt will be skipped. This is known by the engine through metadata, min-max values, and footer (format version, schema, column metadata).

Moreover, Parquet compresses the data using compression algorithms. It further reduces memory footprints:
1. Dictionary Encoding: Creating index values for each word and replace occurrence with these indexes.
2. Run-length Encoding: When data has repeating values consecutive occurrences of the same data value are stored as a single value and a count:
    ```
        # Example usage
        encoded_val = rle_encode('AAAAAAFDDCCCCCCCAEEEEEEEEEEEEEEEEE')
        print(encoded_val) # Output: 6A1F2D7C1A17E
    ```

Moreover, there is Delta format where versioning, audit trails, transaction logs, tracking is maintained.
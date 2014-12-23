def generator_len(generator):
    return None if generator is None else sum(1 for _ in generator)


def chunks(input_data, chunk_size):
    for i in range(0, len(input_data), chunk_size):
        yield input_data[i:i+chunk_size]


def reversed_map(in_map):
    return {value: key for (key, value) in in_map.items()}
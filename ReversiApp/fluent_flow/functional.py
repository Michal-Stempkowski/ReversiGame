def generator_len(generator):
    return None if generator is None else sum(1 for _ in generator)
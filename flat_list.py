def main():
    input = [
        [2, 2, 2, 5, 1],
        [2, 2, 2, 5, 1],
        [2, 2, 2, 5, 1],
    ]
    x = 13
    print(flatten(input, x))


def flatten(nested_list, final_length):
    flat_list = sum(nested_list, [])
    print(flat_list)
    while len(flat_list) > final_length:
        flat_list.pop()

    return flat_list


if __name__ == '__main__':
    main()

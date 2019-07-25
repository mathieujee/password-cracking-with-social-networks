import os


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def write_to_file(filename, content):
    file = open(filename, mode='a', newline='')
    file.write(content + '\n')
    file.close()


def write_list_to_file(filename, list):
    file = open(filename, mode='a', newline='')
    file.write(list)
    file.write('\n')
    file.close()


def write_several_words(filename, content):
    split_content = content.split(' ')
    if len(split_content) > 1:
        for word in split_content:
            if len(word) > 2:
                write_to_file(filename, word)


def read_one_line_from_file(filename):
    file = open(filename, mode='r')
    line = file.readline()
    file.close()
    return line


# src: https://blog.georgechalhoub.com/2015/09/remove-duplicate-lines-from-file-using.html
def remove_duplicate_lines_from_file(filename):
    out = open(filename + '.bis', "w")
    lines_seen = set()
    for line in open(filename, "r"):
        if line not in lines_seen:
            out.write(line)
            lines_seen.add(line)

    remove_file(filename)
    os.rename(filename + '.bis', filename)
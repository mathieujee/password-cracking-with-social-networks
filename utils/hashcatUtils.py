from subprocess import call


def generate_extended_wordlist(source_basic_wordlist_filename, extended_wordlist_filename,
                               hashcat_rules_filename, *, force=1, progress_bar=None):
    command = ['hashcat', '--force', '--stdout', source_basic_wordlist_filename, '-r', hashcat_rules_filename]

    # remove '--force' arg
    if force == 0:
        del command[1]

    output = open(extended_wordlist_filename, "w")
    call(command, stdout=output)
    if progress_bar is not None:
        progress_bar.update(0)


def run_hashcat_rule_attack(hash_filename, hash_type, wordlist_filename, rules_filename, output_filename,
                            *, force=1, potfile=0, progress_bar=None):
    command = ['hashcat']

    if force == 1:
        command.append('--force')
    if potfile == 0:
        command.append('--potfile-disable')

    command += ['-m', hash_type, hash_filename, wordlist_filename, '-r', rules_filename, '-o', output_filename]
    call(command)
    if progress_bar is not None:
        progress_bar.update(0)


def run_hashcat_combinator2_attack(hash_filename, hash_type, wordlist1_filename, worldlist2_filename,
                                   output_filename, *, force=1, potfile=0, progress_bar=None):
    command = ['hashcat']

    if force == 1:
        command.append('--force')
    if potfile == 0:
        command.append('--potfile-disable')

    command += ['-m', hash_type, '-a', '1', hash_filename, wordlist1_filename,
                worldlist2_filename, '-o', output_filename]
    call(command)
    if progress_bar is not None:
        progress_bar.update(0)

    i = command.index('-a')

    # swap wordlists position
    command[i+3], command[i+4] = command[i+4], command[i+3]
    call(command)
    if progress_bar is not None:
        progress_bar.update(0)


def run_hashcat_special_char_combinator_attack(hash_filename, hash_type, wordlist_filename, special_char,
                                               output_filename, *, force=1, potfile=0, progress_bar=None):
    command = ['hashcat']

    if force == 1:
        command.append('--force')
    if potfile == 0:
        command.append('--potfile-disable')

    command += ['-m', hash_type, '-a', '1', hash_filename, '-j', '$' + special_char,
                wordlist_filename, wordlist_filename, '-o', output_filename]

    call(command)
    if progress_bar is not None:
        progress_bar.update(0)


def run_hashcat_special_char_combinator2_attack(hash_filename, hash_type, wordlist1_filename, wordlist2_filename,
                                                special_char, output_filename, *, force=1, potfile=0, progress_bar=None):
    command = ['hashcat']

    if force == 1:
        command.append('--force')
    if potfile == 0:
        command.append('--potfile-disable')

    command += ['-m', hash_type, '-a', '1', hash_filename, '-j', '$' + special_char]

    command_left = command + [wordlist1_filename, wordlist2_filename, '-o', output_filename]
    command_right = command + [wordlist2_filename, wordlist1_filename, '-o', output_filename]

    call(command_left)
    if progress_bar is not None:
        progress_bar.update(0)
    call(command_right)
    if progress_bar is not None:
        progress_bar.update(0)

    # Add special char at the end of the second word
    # command2 = command + ['-k', '$' + special_char]
    # call(command2)

    # Add special chars between the 2 words and at the end of the second one
    # command3 = command + ['-j', '$' + special_char, '-k', '$' + special_char]
    # call(command3)

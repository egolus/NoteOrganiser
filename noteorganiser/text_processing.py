# A post is considered to be extracted from an existing file, and always
# consists in a title, followed by a line of '------------', followed
# immediatly by the tags with a leading #. It is a list of strings, where empty
# ones were removed.
# If it is a valid post, it has at minima 4 lines (title, line of -, tags,
# date)
# They should be extracted recursively, and fed to the different routines
# `_from_post`.
from datetime import date
import re


def is_valid_post(post):
    """
    Check that it has all the required arguments

    >>> good = ["Toto", "-------", "# non-linear, pk", "*21/12/2012*"]
    >>> bad = ["Toto", "-------", "*21/12/2012*"]
    >>> wrong_date = ["Toto", "-----", "# something", "12/12/042*"]
    >>> is_valid_post(good)
    True
    >>> is_valid_post(bad)
    False
    >>> is_valid_post(wrong_date)
    False
    """
    is_valid = True
    if len(post) < 4:
        is_valid = False
    else:
        # Recover the index of the line of dashes, in case of long titles
        index = 0
        dashes = [e for e in post if e.find('----') != -1]
        try:
            index = post.index(dashes[0])
        except ValueError:
            is_valid = False
        if index:
            if not post[0]:
                is_valid = False
            if post[index+1] and post[index+1].find('#') == -1:
                is_valid = False
            if post[index+2]:
                match = re.match(
                    r"\*[0-9]{2}/[0-1][1-9]/[0-9]{4}\*",
                    post[index+2])
                if match is None:
                    is_valid = False
    return is_valid


def extract_tags_from_post(post):
    """
    Recover the tags from an extracted post

    .. note::

        No tests are being done to ensure that the third line exists, as only
        valid posts, determined with :func:`is_valid_post` are sent to this
        routine.

    >>> post = ["Toto", "-------", " # non-linear, pk", "*21/12/2012*"]
    >>> extract_tags_from_post(post)
    ['non-linear', 'pk']
    """
    tag_line = post[2].strip()
    if tag_line and tag_line[0] == '#':
        tags = [elem.strip() for elem in tag_line[1:].split(',')]

    return tags


def extract_title_from_post(post):
    """
    Recover the title from an extracted post

    >>> post = ["Toto", "-------", "# non-linear, pk", "*21/12/2012*"]
    >>> extract_title_from_post(post)
    'Toto'
    """
    return post[0]


def extract_date_from_post(post):
    """
    Recover the date from an extracted post

    >>> post = ["Toto", "-------", "# non-linear, pk", "*21/12/2012*"]
    >>> extract_date_from_post(post)
    datetime.date(2012, 12, 21)
    """
    date_line = post[3]
    match = re.match(
        r"\*([0-9]{2})/([0-1][1-9])/([0-9]{4})\*",
        date_line)
    assert len(match.groups()) == 3
    day, month, year = match.groups()
    extracted_date = date(int(year), int(month), int(day))
    return extracted_date


def normalize_post(post):
    """
    If a title has several lines, merge them

    >>> post = ["Toto", "has a long title", "------", "# something", ]
    >>> normalize_post(post)
    ['Toto has a long title', '------', '# something']
    """
    dashes = [e for e in post if e.find('----') != -1]
    dashline_index = post.index(dashes[0])

    title = ' '.join([post[index] for index in range(dashline_index)])
    normalized_post = [title]
    normalized_post.extend(post[dashline_index:])

    return normalized_post


def extract_corpus_from_post(post):
    """
    Recover the whole content of a post

    >>> post = ["Toto", "-------", "# non-linear, pk", "*21/12/2012*",
    ...         "This morning I woke", "up and it was a nice weather"]
    >>> extract_corpus_from_post(post)
    ['This morning I woke', 'up and it was a nice weather']
    """
    return post[4:]


def extract_title_and_posts_from_text(text):
    """
    From an entire text (array), recover each posts and the file's title

    """
    # Make a first pass to recover the title (first line that is underlined
    # with = signs) and the indices of the dash, that signals a new post.
    post_starting_indices = []
    for index, line in enumerate(text):
        # Remove white lines at the beginning
        if not line:
            continue
        if line.find("====") != -1:
            title = text[index-1]
        if line.find('----') != -1 and line[0] == '-':
            post_starting_indices.append(index-1)
    print post_starting_indices
    number_of_posts = len(post_starting_indices)

    # Create post_indices such that it stores all the post, so the starting and
    # ending index of each post
    post_indices = []
    for index, elem in enumerate(post_starting_indices):
        if index < number_of_posts - 1:
            post_indices.append([elem, post_starting_indices[index+1]])
        else:
            post_indices.append([elem, len(text)])

    posts = []
    for elem in post_indices:
        start, end = elem
        posts.append(text[start:end])

    return title, posts

if __name__ == "__main__":
    import doctest
    doctest.testmod()
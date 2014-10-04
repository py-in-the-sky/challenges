from evernote import *

NOTE1 = """<note>
  <guid>6BA8DC47-EB38-40D9-BE32-5D5DD82E9EC7</guid>
  <created>2013-07-12T19:22:13Z</created>
  <tag>poetry</tag>
  <tag>whitman</tag>
  <content>
    Gliding o'er all, through all,
    Through Nature, Time, and Space,
    As a ship on the waters advancing,
    The voyage of the soul - not life alone,
    Death, many deaths I'll sing.
    And some other words for indexing.
  </content>
</note>"""

NOTE2 = """<note>
  <guid>450E1369-9D9D-4168-8969-2A4DCC8DDEC4</guid>
  <created>2014-04-29T08:37:16Z</created>
  <tag>poetry</tag>
  <tag>byron</tag>
  <content>
    Famed for their civil and domestic quarrels
    See heartless Henry lies by headless Charles;
    Between them stands another sceptred thing,
    It lives, it reigns - "aye, every inch a king."
    Charles to his people, Henry to his wife,
    In him the double tyrant starts to life:
    Justice and Death have mixed their dust in vain.
    The royal Vampires join and rise again.
    What now can tombs avail, since these disgorge
    The blood and dirt of both to mould a George!
  </content>
</note>"""

def test():
    note1, note2 = parse_note(NOTE1), parse_note(NOTE2)

    assert note1['guid'] == '6BA8DC47-EB38-40D9-BE32-5D5DD82E9EC7'
    assert 'poetry' in note2['tag']
    assert 'for' in set.intersection(note1['content'], note2['content'])

    trie1 = tree()
    trie_delete('blah', 'blah', trie1)  # just make sure no error thrown
    assert get_word('none', trie1) is NULL_GUIDS
    assert find_trie('none', trie1) == tree()
    assert 'n' in trie1 and 'e' in find_trie('non', trie1)
    trie_put('to', 'to', trie1)
    trie_put('toes', 'toes', trie1)
    assert 'to' in get_word('to', trie1) and 'toes' not in get_word('to', trie1)
    assert 'to' in get_prefix('to', trie1) and 'toes' in get_prefix('to', trie1)
    trie_delete('to', 'to', trie1)
    assert 'to' not in get_prefix('to', trie1) and 'toes' in get_prefix('to', trie1)
    trie_put('toes', 'toes2', trie1)
    assert 'toes' in get_word('toes', trie1) and 'toes2' in get_word('toes', trie1)

    trie2 = tree()
    words = 'aaa aab aac aaa abb abc acc acb'.split()
    pivot = 'aac'
    for w in words:
      trie_put(w, w, trie2)
    gte = get_gte(pivot, trie2)
    assert 'aac' in gte and 'abb' in gte and 'acb' in gte and 'aab' not in gte
    gte2 = get_gte('aaaa', trie2)
    assert 'aac' in gte2 and 'aaa' not in gte2 and 'aaaa' not in gte2

    create(note1)
    create(note2)
    content = indexes['content']
    assert '6BA8DC47-EB38-40D9-BE32-5D5DD82E9EC7' in get_word('for', content)
    assert '450E1369-9D9D-4168-8969-2A4DCC8DDEC4' in get_word('for', content)
    query = 'civil fo*'
    queries = (parse_query(qs) for qs in query.split())
    intersection = search_intersection(queries)
    assert '450E1369-9D9D-4168-8969-2A4DCC8DDEC4' in intersection
    assert '6BA8DC47-EB38-40D9-BE32-5D5DD82E9EC7' not in intersection

    queries2 = (parse_query(qs) for qs in 'tag:poetry'.split())
    intersection2 = search_intersection(queries2)
    assert '450E1369-9D9D-4168-8969-2A4DCC8DDEC4' in intersection2
    assert '6BA8DC47-EB38-40D9-BE32-5D5DD82E9EC7' in intersection2

    queries3 = (parse_query(qs) for qs in 'tag:blah'.split())
    assert len(search_intersection(queries3)) == 0
    queries4 = (parse_query(qs) for qs in 'tag:Poetry'.split())
    assert len(search_intersection(queries4)) == 2

    return 'tests pass!'


if __name__ == '__main__':
    print test()

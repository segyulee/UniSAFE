from unisafe.io import read_jsonl, write_jsonl


def test_jsonl_round_trip(tmp_path):
    path = tmp_path / "rows.jsonl"
    write_jsonl(path, [{"id": "한글"}, {"id": "two"}])
    assert list(read_jsonl(path)) == [{"id": "한글"}, {"id": "two"}]

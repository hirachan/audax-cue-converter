from audax_cue_converter.rwgps import get_sign


def test_1():
    s = "左折する (福島県農業総合センター の表示)"
    expect = "福島県農業総合センター"

    assert get_sign(s) == expect


def test_2():
    s = "右折して郡山東部広域農道に入る (磐越自動車道/須賀川/国道49号 の表示)"
    expect = "磐越自動車道・須賀川・国道49号"

    assert get_sign(s) == expect


def test_3():
    s = "Turn right onto 県道13号 (signs for 国道49号線)"
    expect = "国道49号線"

    assert get_sign(s) == expect

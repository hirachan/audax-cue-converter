from audax_cue_converter.rwgps import get_road


def test_1():
    s = "右折して国道4号に入る"
    expect = ("", "N4")

    assert get_road(s) == expect


def test_2():
    s = "左折して 県道54号 に向かう"
    expect = ("", "CR")

    assert get_road(s) == expect


def test_3():
    s = "右折して郡山東部広域農道に入る (磐越自動車道/須賀川/国道49号 の表示)"
    expect = ("郡山東部広域農道", "AR")

    assert get_road(s) == expect


def test_4():
    s = "谷田川（交差点） を左折して 国道49号 に入る (日立/いわき/空港 の表示)"
    expect = ("", "N49")

    assert get_road(s) == expect


def test_5():
    s = "県道56号線を進む"
    expect = ("", "D56")

    assert get_road(s) == expect


def test_6():
    s = "ロータリーの3 つ目の出口を出て よかっぺ通り/県道290号 に入る"
    expect = ("よかっぺ通り", "D290")

    assert get_road(s) == expect


def test_7():
    s = "回春荘病院前（交差点）を直進して、そのまま一本松通りへ進む"
    expect = ("一本松通り", "CR")

    assert get_road(s) == expect


def test_8():
    s = "八街十字路（交差点）で県道22号線へ進む"
    expect = ("", "D22")

    assert get_road(s) == expect


def test_9():
    s = "斜め左方向に曲がり県道110号に入る"
    expect = ("", "D110")

    assert get_road(s) == expect


def test_10():
    s = "十倉（交差点） を左折してそのまま 県道45号線 を進む"
    expect = ("", "D45")

    assert get_road(s) == expect


def test_11():
    s = "大清水（交差点） で斜め左に折れて 県道43号線 に入る"
    expect = ("", "D43")

    assert get_road(s) == expect

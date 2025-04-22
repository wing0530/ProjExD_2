import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんrect or 爆弾rect
    戻り値：rectが画面内ならTrue 外ならFalseのタプル
    """
    yoko, tate = True, True
    # 横判定
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    # 縦判定
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen):
    """
    引数：大元のスクリーン
    戻り値：終了
    """
    # ブラックアウト
    bo_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bo_img, (0, 0, 0), (0, 0, 1100, 650))
    bo_img.set_alpha(128)
    bo_rct = bo_img.get_rect()
    # gameover
    fnt = pg.font.Font(None, 80)
    txt = fnt.render("GAME OVER", True, (255, 255, 255))
    # 負けかとん
    mk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    mk_rct = mk_img.get_rect()
    mk_rct.center = 300, 200
    print("GameOver")
    screen.blit(bo_img, bo_rct)
    screen.blit(txt, [400, HEIGHT / 2])
    screen.blit(mk_img, [WIDTH * 1 / 3 - 20, HEIGHT / 2])
    screen.blit(mk_img, [WIDTH * 2 / 3 + 20, HEIGHT / 2])
    pg.display.update()
    pg.time.wait(5000)
    return


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：弾イラストのリストと加速度のリスト
    """
    bb_accs = [a for a in range(1, 11)]  # 加速率を設定 (1〜10)
    bb_imgs = []
    for r in range(1, 11):
        # 爆弾描画
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    # ろーてかとん
    rk_img = pg.image.load("fig/3.png")
    f_rk_img = pg.transform.flip(rk_img, True, False)
    rk_imgs = {
        (+5,0): pg.transform.rotozoom(f_rk_img, 0, 0.9),
        (+5,+5):pg.transform.rotozoom(f_rk_img, -45, 0.9),
        (0,+5):pg.transform.rotozoom(f_rk_img, -90, 0.9),
        (-5,+5):pg.transform.rotozoom(rk_img, 45, 0.9),
        (-5,0):pg.transform.rotozoom(rk_img, 0, 0.9),
        (-5,-5):pg.transform.rotozoom(rk_img, -45, 0.9),
        (0,-5):pg.transform.rotozoom(rk_img, -90, 0.9),
        (+5,-5):pg.transform.rotozoom(f_rk_img, 45, 0.9)
    }
    return rk_imgs.get(sum_mv, rk_img)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    # 爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect() 
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 初期位置
    vx, vy = +5, +5  # 初期速度

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = get_kk_img(tuple(sum_mv))
        screen.blit(kk_img, kk_rct)

        # 爆弾移動
        avx = vx * bb_accs[min(tmr // 500, 9)]  
        avy = vy * bb_accs[min(tmr // 500, 9)]  

        # 爆弾の移動
        bb_rct.move_ip(avx, avy)

        # 画面端
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_imgs[min(tmr // 500, 9)], bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)

        # 接触による終了
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

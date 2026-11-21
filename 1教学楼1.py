import bpy

for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT_DIR = ARGS[0] if ARGS else r"E:\Blender Works\Demo"
TEX_DIR = os.path.join(OUT_DIR, "textures")
os.makedirs(TEX_DIR, exist_ok=True)

random.seed(20261112)

LOG = os.path.join(OUT_DIR, "生成日志.txt")
def log(*a):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(" ".join(str(x) for x in a) + "\n")
    except Exception:
        pass
open(LOG, "w", encoding="utf-8").close()

def now():
    return round(time.time() - T0, 1)

T0 = time.time()
log("开始", time.strftime("%Y-%m-%d %H:%M:%S"))

#材质贴图
def periodic_noise(res, cells, seed):
    rng = np.random.default_rng(seed)
    grid = rng.random((cells, cells)).astype(np.float32)
    x = np.linspace(0, cells, res, endpoint=False, dtype=np.float32)
    xi = np.floor(x).astype(np.int32) % cells
    xf = x - np.floor(x)
    xf = xf * xf * (3 - 2 * xf)
    xj = (xi + 1) % cells
    g00 = grid[np.ix_(xi, xi)]
    g10 = grid[np.ix_(xi, xj)]
    g01 = grid[np.ix_(xj, xi)]
    g11 = grid[np.ix_(xj, xj)]
    fx = xf[None, :]
    fy = xf[:, None]
    a = g00 * (1 - fx) + g10 * fx
    b = g01 * (1 - fx) + g11 * fx
    return a * (1 - fy) + b * fy

def fbm(res, seed, base=4, octaves=5):
    out = np.zeros((res, res), np.float32)
    amp = 0.5
    total = 0.0
    for i in range(octaves):
        out += periodic_noise(res, base * (2 ** i), seed + i * 31) * amp
        total += amp
        amp *= 0.5
    return out / total

def blur(a, r=3):
    if r <= 0:
        return a
    k = 2 * r + 1
    p = np.pad(a, r, mode="wrap")
    c = np.cumsum(p, axis=0)
    c = np.vstack([np.zeros((1, c.shape[1]), np.float32), c])
    a1 = (c[k:, :] - c[:-k, :]) / k
    c = np.cumsum(a1, axis=1)
    c = np.hstack([np.zeros((c.shape[0], 1), np.float32), c])
    return (c[:, k:] - c[:, :-k]) / k

def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

def save_tex(name, color, rough):
    h, w, _ = color.shape
    img = bpy.data.images.new(name, width=w, height=h, alpha=False)
    rgba = np.ones((h, w, 4), np.float32)
    rgba[:, :, :3] = np.clip(color, 0, 1)
    img.pixels.foreach_set(rgba.ravel())
    img.filepath_raw = os.path.join(TEX_DIR, name + ".png")
    img.file_format = "PNG"
    img.save()
    rimg = bpy.data.images.new(name + "_R", width=w, height=h, alpha=False)
    r4 = np.ones((h, w, 4), np.float32)
    r4[:, :, 0] = rough
    r4[:, :, 1] = rough
    r4[:, :, 2] = rough
    rimg.pixels.foreach_set(r4.ravel())
    rimg.filepath_raw = os.path.join(TEX_DIR, name + "_R.png")
    rimg.file_format = "PNG"
    rimg.save()
    return os.path.join(TEX_DIR, name + ".png"), os.path.join(TEX_DIR, name + "_R.png")

def make_textures():
    # 乳白墙面
    R = 512
    n1 = fbm(R, 3, 4, 6)
    n2 = fbm(R, 11, 16, 3)
    base = np.array([0.955, 0.935, 0.895], np.float32)
    dirt = np.array([0.800, 0.775, 0.725], np.float32)
    m = np.clip((n1 - 0.42) * 1.4, 0, 1) * 0.20 + n2 * 0.05
    wall = base[None, None, :] * (1 - m[:, :, None]) + dirt[None, None, :] * m[:, :, None]
    wall *= (0.988 + 0.024 * n2[:, :, None])
    wall_r = np.clip(0.64 + (n1 - 0.5) * 0.16 + (n2 - 0.5) * 0.08, 0.5, 0.82)
    wall_c, wall_rp = save_tex("wall_plaster", wall, wall_r)

    # 大理石
    R = 1024
    u, v = np.meshgrid(np.linspace(0, 1, R, endpoint=False),
                       np.linspace(0, 1, R, endpoint=False))
    cloud = fbm(R, 101, 2, 5)
    warp = fbm(R, 202, 3, 5)
    fine = fbm(R, 303, 8, 4)
    p1 = (u * 1.6 + v * 0.45 + (warp - 0.5) * 2.6) * math.pi * 2
    s1 = np.sin(p1)
    vein1 = np.exp(-((s1 / (0.15 + 0.07 * cloud)) ** 2))
    p2 = (u * 4.2 - v * 1.3 + (cloud - 0.5) * 3.0) * math.pi * 2
    vein2 = np.exp(-((np.sin(p2) / 0.06) ** 2)) * 0.40
    mask = smoothstep(0.2, 0.8, fbm(R, 404, 2, 3))
    vein = np.clip(blur(vein1 * (0.35 + 0.65 * mask) + vein2, 2), 0, 1)

    baseW = np.array([0.890, 0.878, 0.852], np.float32)
    darkW = np.array([0.515, 0.500, 0.475], np.float32)
    colW = np.ones((R, R, 3), np.float32) * baseW[None, None, :]
    colW *= (0.95 + 0.08 * cloud[:, :, None])
    colW = colW * (1 - vein[:, :, None] * 0.50) + darkW[None, None, :] * (vein[:, :, None] * 0.50)
    colW += (fine[:, :, None] - 0.5) * 0.010
    roughW = np.clip(0.17 + vein * 0.13 + (cloud - 0.5) * 0.05, 0.10, 0.34)
    white_c, white_r = save_tex("marble_white", colW, roughW)

    baseD = np.array([0.110, 0.107, 0.116], np.float32)
    lightD = np.array([0.470, 0.455, 0.440], np.float32)
    colD = np.ones((R, R, 3), np.float32) * baseD[None, None, :]
    colD *= (0.80 + 0.40 * cloud[:, :, None])
    colD = colD * (1 - vein[:, :, None] * 0.55) + lightD[None, None, :] * (vein[:, :, None] * 0.55)
    roughD = np.clip(0.20 + vein * 0.12 + (cloud - 0.5) * 0.05, 0.12, 0.36)
    dark_c, dark_r = save_tex("marble_dark", colD, roughD)

    # 吊顶矿棉板
    R = 512
    n = fbm(R, 33, 4, 5)
    cc = np.array([0.870, 0.858, 0.828], np.float32)
    ceil = np.ones((R, R, 3), np.float32) * cc[None, None, :]
    ceil *= (0.96 + 0.05 * n[:, :, None])
    grid = np.ones((R, R), np.float32)
    for k in range(0, R, 128):
        grid[k:k + 3, :] = 0.70
        grid[:, k:k + 3] = 0.70
    ceil *= grid[:, :, None]
    ceil_r = np.clip(0.88 + (n - 0.5) * 0.06, 0.8, 0.95)
    ceil_c, ceil_rp = save_tex("ceiling_tile", ceil, ceil_r)

    # 深色木纹
    R = 512
    nw = fbm(R, 44, 4, 5)
    xx = np.linspace(0, 40, R, dtype=np.float32)
    grain = 0.5 + 0.5 * np.sin((xx[None, :] * 1.5 + nw * 9) * math.pi)
    wb = np.array([0.285, 0.180, 0.115], np.float32)
    wd = np.array([0.150, 0.092, 0.058], np.float32)
    wood = wb[None, None, :] * (1 - grain[:, :, None] * 0.55) + wd[None, None, :] * (grain[:, :, None] * 0.55)
    wood_r = np.clip(0.42 + (nw - 0.5) * 0.12, 0.32, 0.55)
    wood_c, wood_rp = save_tex("wood_dark", wood, wood_r)

    # 混凝土
    R = 512
    nc = fbm(R, 55, 5, 5)
    cb = np.array([0.470, 0.462, 0.445], np.float32)
    cd = np.array([0.330, 0.322, 0.310], np.float32)
    conc = cb[None, None, :] * (0.97 + 0.05 * nc[:, :, None])
    conc += (fbm(R, 77, 24, 2)[:, :, None] - 0.5) * 0.012
    conc_r = np.clip(0.84 + (nc - 0.5) * 0.05, 0.78, 0.9)
    conc_c, conc_rp = save_tex("concrete", conc, conc_r)

    # 卫生间小瓷砖
    R = 512
    nt = fbm(R, 66, 6, 4)
    tb = np.array([0.780, 0.790, 0.760], np.float32)
    tile = np.ones((R, R, 3), np.float32) * tb[None, None, :]
    tile *= (0.90 + 0.18 * nt[:, :, None])
    g = np.ones((R, R), np.float32)
    for k in range(0, R, 64):
        g[k:k + 3, :] = 0.55
        g[:, k:k + 3] = 0.55
    tile *= g[:, :, None]
    tile_r = np.full((R, R), 0.28, np.float32)
    tile_c, tile_rp = save_tex("tile_wc", tile, tile_r)

    return {
        "wall": (wall_c, wall_rp),
        "marble_white": (white_c, white_r),
        "marble_dark": (dark_c, dark_r),
        "ceiling": (ceil_c, ceil_rp),
        "wood": (wood_c, wood_rp),
        "concrete": (conc_c, conc_rp),
        "tile": (tile_c, tile_rp),
    }

log("生成贴图")
TEX = make_textures()
log("0", now())

#材质
def pbr(name, color, rough, metallic=0.0, emission=None, strength=0.0, alpha=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (emission[0], emission[1], emission[2], 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        try:
            mat.surface_render_method = 'BLENDED'
        except Exception:
            pass
    return mat

def image_mat(name, color_path, rough_path=None, metallic=0.0, bump=0.0, emit=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Metallic"].default_value = metallic
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(color_path, check_existing=True)
    tex.image.colorspace_settings.name = "sRGB"
    tex.interpolation = "Linear"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if rough_path is not None:
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = bpy.data.images.load(rough_path, check_existing=True)
        tr.image.colorspace_settings.name = "Non-Color"
        nt.links.new(tr.outputs["Color"], bsdf.inputs["Roughness"])
    if emit > 0:
        bsdf.inputs["Emission Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = emit
    if bump > 0:
        bmp = nt.nodes.new("ShaderNodeBump")
        bmp.inputs["Strength"].default_value = bump
        bmp.inputs["Distance"].default_value = 0.02
        nt.links.new(tex.outputs["Color"], bmp.inputs["Height"])
        nt.links.new(bmp.outputs["Normal"], bsdf.inputs["Normal"])
    return mat

log("创建材质")
M = {}
M["wall"] = image_mat("M_乳白墙面", TEX["wall"][0], TEX["wall"][1], bump=0.05, emit=0.08)
M["wall_dirty"] = pbr("M_脏墙", (0.52, 0.48, 0.42), 0.85)
M["marble_white"] = image_mat("M_白色大理石", TEX["marble_white"][0], TEX["marble_white"][1], emit=0.025)
M["marble_dark"] = image_mat("M_深色大理石", TEX["marble_dark"][0], TEX["marble_dark"][1], emit=0.02)
M["ceiling"] = image_mat("M_吊顶", TEX["ceiling"][0], TEX["ceiling"][1], emit=0.42)

M["concrete"] = image_mat("M_混凝土", TEX["concrete"][0], TEX["concrete"][1], bump=0.08, emit=0.08)
M["tile"] = image_mat("M_卫生间瓷砖", TEX["tile"][0], TEX["tile"][1], emit=0.04)
M["wood"] = image_mat("M_深色木", TEX["wood"][0], TEX["wood"][1])
M["wood_light"] = pbr("M_浅木", (0.36, 0.24, 0.15), 0.55)
M["metal"] = pbr("M_金属", (0.18, 0.18, 0.19), 0.42, metallic=0.85)
M["metal_dark"] = pbr("M_深金属", (0.07, 0.07, 0.08), 0.5, metallic=0.7)
M["rust"] = pbr("M_锈", (0.31, 0.14, 0.06), 0.85)
M["glass"] = pbr("M_玻璃", (0.55, 0.62, 0.65), 0.06, metallic=0.1, alpha=0.16)
M["glass_broken"] = pbr("M_脏玻璃", (0.35, 0.40, 0.40), 0.35, alpha=0.45)
M["blackboard"] = pbr("M_黑板", (0.045, 0.075, 0.060), 0.42)
M["blackboard_frame"] = pbr("M_黑板框", (0.30, 0.19, 0.10), 0.5)
M["paper"] = pbr("M_纸", (0.78, 0.74, 0.63), 0.9)
M["paper_old"] = pbr("M_旧纸", (0.58, 0.52, 0.40), 0.95)
M["fabric"] = pbr("M_布", (0.10, 0.10, 0.12), 0.9)
M["fabric_red"] = pbr("M_红布", (0.22, 0.03, 0.03), 0.85)
M["blood"] = pbr("M_血", (0.055, 0.004, 0.003), 0.34)
M["blood_dry"] = pbr("M_干血", (0.030, 0.006, 0.005), 0.7)
M["light"] = pbr("M_灯管", (0.85, 0.92, 0.95), 0.3, emission=(0.75, 0.88, 1.0), strength=6.0)
M["light_off"] = pbr("M_灯管坏", (0.20, 0.21, 0.22), 0.6)
M["light_red"] = pbr("M_应急灯", (0.5, 0.02, 0.02), 0.4, emission=(1.0, 0.03, 0.02), strength=8.0)
M["plant"] = pbr("M_枯叶", (0.16, 0.18, 0.09), 0.9)
M["soil"] = pbr("M_土", (0.09, 0.07, 0.05), 1.0)
M["skin"] = pbr("M_人偶", (0.62, 0.55, 0.46), 0.55)
M["bodybag"] = pbr("M_裹尸袋", (0.025, 0.025, 0.028), 0.38)
M["chalk"] = pbr("M_粉笔", (0.9, 0.9, 0.85), 0.9)
M["screen"] = pbr("M_投影幕", (0.72, 0.72, 0.68), 0.9)
M["asphalt"] = pbr("M_沥青", (0.045, 0.045, 0.048), 0.95)
M["grass"] = pbr("M_枯草", (0.10, 0.10, 0.06), 1.0)
M["tree"] = pbr("M_枯树", (0.10, 0.075, 0.055), 0.95)
M["red"] = pbr("M_消防红", (0.42, 0.03, 0.02), 0.4, metallic=0.2)
M["mirror"] = pbr("M_镜子", (0.55, 0.58, 0.60), 0.05, metallic=1.0)
M["ceramic"] = pbr("M_陶瓷", (0.72, 0.72, 0.68), 0.18)
M["black"] = pbr("M_黑", (0.012, 0.012, 0.013), 0.5)
M["water"] = pbr("M_积水", (0.012, 0.016, 0.020), 0.03, metallic=0.25)
M["locker"] = pbr("M_储物柜", (0.24, 0.29, 0.27), 0.6, metallic=0.2)
M["door"] = pbr("M_门", (0.23, 0.15, 0.09), 0.5)

import taichi as ti
import taichi.math as tm
ti.init(arch=ti.gpu)

import engine

res = 512
# A global 2D field of 3D vectors representing RGB colors for each pixel
pixels = ti.Vector.field(3, dtype=float, shape=(res, res))

@ti.kernel
def background():
    for i, j in pixels:
        pixels[i, j] = ti.Vector([0., 0., 0.])

@ti.func
def calculate_quad(a:float, b:float, c:float):
    hit = False
    t = 0.

    discriminant = b**2 - (4*a*c)

    if discriminant >= 0.:
        t_neg = (-b - tm.sqrt(discriminant)) / (2 * a)
        t_pos = (-b + tm.sqrt(discriminant)) / (2 * a)

        if t_neg > 0 and t_pos > 0:
            hit = True
            t = min(t_neg, t_pos)
        elif t_neg > 0:
            hit = True
            t = t_neg
        elif t_pos > 0:
            hit = True
            t = t_pos
        else:
            hit = False
            t = 0.0

    return hit, t

@ti.kernel
def render_sphere(radius: float, sphere_pos : ti.types.vector(3, float), color : ti.types.vector(3, float)): # type: ignore
    camera_pos = ti.Vector([0., 0., 10.])
    for i, j in pixels:
        screen_x = (float(i) - res / 2) / res
        screen_y = (float(j) - res / 2) / res

        ray_origin = camera_pos

        ray_direction = ti.Vector([
            screen_x,
            screen_y,
            -1.
        ]).normalized()

        a = ray_direction.dot(ray_direction)
        b = 2.0 * (ray_origin - sphere_pos).dot(ray_direction)
        c = (ray_origin - sphere_pos).dot(ray_origin - sphere_pos) - radius**2

        hit, t = calculate_quad(a, b, c)
        if hit:
            hit_point = ray_origin + t * ray_direction
            normal = (hit_point - sphere_pos).normalized()

            light_dir = ti.Vector([0.1, 0.2, 0.6]).normalized()
            intensity = max(0.0, normal.dot(light_dir))

            pixels[i, j] = color * intensity

gui = ti.GUI("2D Sphere Shader", res=(res, res))
while gui.running:
    center = res // 2
    dt = 0.002

    engine.calculate_forces()
    engine.calculate_accel()

    engine.update_velocity(dt)
    engine.update_position(dt)

    # Clear the frame
    background()

    # Draw the current state
    render_sphere(
        1., 
        engine.positions[0], 
        ti.Vector([0., 0., 1.]))
    
    render_sphere(
        1.,
        engine.positions[1],
        ti.Vector([1., 0., 0.]))

    render_sphere(
            1.,
            engine.positions[2],
            ti.Vector([0., 1., 0.]))

    gui.set_image(pixels) # Displays the updated pixel field immediately
    gui.show()

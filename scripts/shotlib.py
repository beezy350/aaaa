"""Be Bold shot-language arsenal: camera angles, lens tricks, lighting and formats.
Each entry = the emotion it creates + the prompt fragment that gets the image model to shoot it.
Use: from shotlib import shot, light; prompt = BASE + shot('low_angle') + light('rembrandt') + subject
Rule: pick the shot for the EMOTION of the line, not at random (Nov 18, owner's reference set)."""

SHOTS = {
 # framing / distance
 'wide':          ('Belonging or exposure', 'wide-angle establishing shot, small subject centered in a vast environment, strong leading lines, deep perspective'),
 'medium':        ('Natural interaction',   'medium shot from the waist up, eye-level, relaxed natural framing'),
 'close_up':      ('Intimacy',              'close-up on the face or subject filling the frame, shallow depth of field, every detail readable'),
 'extreme_cu':    ('Intense focus',         'extreme close-up macro of a single detail (an eye, a hand-free object, a crack), razor-thin focus'),
 'negative_space':('Emptiness',             'subject small at one edge of the frame, huge empty sky or sea filling the rest, minimal composition'),
 # camera angle
 'low_angle':     ('Power or threat',       'low-angle shot looking up at the subject, towering over the camera, sky and buildings converging behind'),
 'high_angle':    ('Vulnerability',         'high-angle shot looking down on the subject, small and exposed, walls closing in'),
 'overhead':      ('Powerlessness',         "top-down bird's-eye overhead shot, subject still at the center while the world moves around"),
 'dutch':         ('Unease',                'dutch angle, camera tilted about 20 degrees, horizon and lines slanted, off-balance'),
 'pov':           ('Immersion',             'first-person point-of-view shot, the viewer sees exactly what the subject sees'),
 'ots':           ('Social interaction',    'over-the-shoulder shot, blurred shoulder and head in the foreground, the other subject sharp facing camera'),
 # movement (for video frames / motion blur in stills)
 'tracking':      ('Momentum',              'tracking shot alongside the moving subject, background streaked with motion blur, subject sharp'),
 'handheld':      ('Nervous energy',        'handheld documentary feel, slightly off-level, crowded busy street, raw and immediate'),
 'slow_motion':   ('Heightened emotion',    'frozen high-speed moment, water droplets or dust suspended in the air, crisp detail'),
 'dolly_zoom':    ('Disorientation',        'dolly-zoom vertigo look, subject the same size while the background stretches away, corridor perspective warped'),
 # lens tricks
 'long_lens':     ('Trapped feeling',       'long telephoto lens compression, crowd and traffic stacked tightly behind the subject, background compressed'),
 'rack_focus':    ('Shifting attention',    'shallow focus with a blurred foreground object and the subject sharp behind it, bokeh lights'),
 'silhouette':    ('Mystery',               'full silhouette against a bright window or sunset, no visible face detail, strong outline'),
}

LIGHT = {
 'rembrandt':   ('Gravity, wisdom',     'Rembrandt lighting, single key light at 45 degrees, small triangle of light on the shadow side'),
 'chiaroscuro': ('Inner conflict',      'chiaroscuro, deep black shadows and one hard beam of light, high contrast'),
 'rim':         ('Isolation, edge',     'strong rim backlight outlining the subject, face in shadow, glowing edges'),
 'golden_hour': ('Hope, nostalgia',     'golden hour, low warm sun, long shadows, amber haze'),
 'blue_hour':   ('Melancholy, calm',    'blue hour, cold blue sky after sunset, warm practical lights starting to glow'),
 'candle':      ('Solitude, reflection','lit only by candle or a single practical lamp, warm pool of light, darkness around'),
 'top_light':   ('Interrogation, fate', 'harsh single top light from directly above, eyes in shadow, spotlight on the floor'),
 'god_rays':    ('Revelation',          'volumetric god rays through dust or fog, beams cutting the darkness'),
 'low_key':     ('Danger, secrets',     'low-key lighting, mostly black frame, only key shapes lit'),
 'high_key':    ('Clarity, openness',   'soft high-key light, bright even exposure, airy'),
 'neon_rain':   ('Modern loneliness',   'night rain, neon reflections on wet asphalt, cyan and magenta glow'),
 'window':      ('Honesty, quiet',      'soft motivated window light from one side, gentle falloff, natural'),
 'storm':       ('Turmoil',             'storm light, heavy dark clouds, a single break of sun, wind'),
}

FORMATS = {
 'triptych_carousel': '3 stacked cinematic panels per slide, each labeled with SHOT NAME + a yellow emotion tag (cameratricks style). Same subject across panels so only the camera changes. Renderer: scripts/render/triptych.py',
 'one_subject_three_feelings': 'Same scene shot three ways (e.g. low angle / high angle / overhead) to show how a single situation feels powerful vs weak vs lost — great for Stoic "perception is a choice" posts.',
 'shot_reveal_reel': 'Reel: start wide, punch to close-up, end on extreme close-up of the eye on the punchline.',
}

def shot(key): return SHOTS[key][1] + '. '
def light(key): return LIGHT[key][1] + '. '
def emotion(key): return (SHOTS.get(key) or LIGHT.get(key))[0]

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

# ---------------- DOODLE ARSENAL (viral hand-drawn formats, research Nov 19, 2026) ----------------
DOODLE_LOOKS = {
 'pencil_doodle': 'hand-drawn doodle in colored pencil and marker, childlike scribbly hatching, thick wobbly black outlines, bright flat colors, pure white background, no text',
 'stick_figure':  'minimal black stick-figure drawing, round head, thin confident marker lines, one accent color (orange tie or red cap), clean white background, no text',
 'whiteboard':    'black dry-erase marker line art on a clean whiteboard, simple shapes, no shading, no text',
 'chalkboard':    'white chalk line drawing on a dark green-black chalkboard with faint chalk dust, no text',
 'grid_paper':    'thin black ink stick figures on light grey grid notebook paper, a few highlighter accents, no text',
 'blueprint':     'white technical line drawing on a deep blue blueprint grid, no text',
}
DOODLE_FORMATS = {
 'list_rows':     'numbered handwritten rules, 3 per page, text one side + doodle the other, rows alternate (scripts/render/doodle.py)',
 'levels':        '"Every level of X" — a labeled staircase/building, stick figure climbs one level per line, camera tilts up level by level (4.6M "every level of manipulation", 1.4M "levels of consciousness")',
 'split_compare': 'split screen, two stick figures doing the same thing with opposite outcomes (car vs seed 1.1M, quitter one metre short of gold 2.1M)',
 'race_labels':   'two labeled figures ("OBSESSION" vs "DISCIPLINE") race up stairs / along a road; the label words carry the meaning (2.2M, 128K)',
 'metaphor_story':'one stick figure acts out a psychology concept as a short story: problem → visual metaphor → principle → takeaway (crabs in a bucket 290K, rock bottom vs fine 197K, loyalty paradox 566K)',
 'timeline':      'left-to-right timeline that grows (PAYDAY → year 1 → year 5), the figure gets taller/richer each step (165K)',
 'pan_mural':     'one long hand-drawn scene; the camera pans across it as the story moves, objects draw themselves in on cue',
}
DOODLE_MOVES = 'draw-on line reveal, colour hatching sweep, handwriting write-on synced to voice, label pop-in, number counter, slow push-in, tilt up a tall drawing, horizontal pan across a mural, split-screen wipe, final page hold; no sound effects'

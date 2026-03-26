#!/usr/bin/env python3
"""
Database Seeding Script
Initial data for pain categories and exercises
"""

import json
from app import db, create_app
from app.models.exercise import PainCategory, Exercise

def seed_database():
    """Seed database with initial yoga pose data."""
    
    print("Seeding database...")
    
    # Pain Categories
    categories_data = [
        {
            'name': 'Neck Pain',
            'description': 'Gentle exercises to relieve neck tension and pain',
            'icon': 'neck_icon',
            'color': '#8B9A7C'
        },
        {
            'name': 'Back Pain',
            'description': 'Strengthening and stretching poses for back relief',
            'icon': 'back_icon',
            'color': '#9B8FBF'
        },
        {
            'name': 'Shoulder Pain',
            'description': 'Exercises to improve shoulder mobility and reduce pain',
            'icon': 'shoulder_icon',
            'color': '#D4A574'
        },
        {
            'name': 'Knee Pain',
            'description': 'Low-impact poses to strengthen knees and reduce discomfort',
            'icon': 'knee_icon',
            'color': '#7CAF9B'
        },
        {
            'name': 'Stress Relief',
            'description': 'Calming poses to reduce stress and anxiety',
            'icon': 'stress_icon',
            'color': '#AF8B9A'
        },
        {
            'name': 'General Wellness',
            'description': 'Overall body strengthening and flexibility exercises',
            'icon': 'general_icon',
            'color': '#8BAF8B'
        }
    ]
    
    # Create categories
    category_map = {}
    for cat_data in categories_data:
        existing = PainCategory.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = PainCategory(**cat_data)
            db.session.add(category)
            db.session.flush()
            category_map[cat_data['name']] = category.id
            print(f"  Created category: {cat_data['name']}")
        else:
            category_map[cat_data['name']] = existing.id
            print(f"  Category exists: {cat_data['name']}")
    
    # Exercises
    exercises_data = [
        # Neck Pain
        {
            'name': 'Camel Pose',
            'sanskrit_name': 'Ustrasana',
            'description': 'A kneeling backbend that stretches the entire front of the body, including the neck.',
            'benefits': json.dumps(['Relieves neck tension', 'Opens chest', 'Improves posture', 'Strengthens back']),
            'instructions': json.dumps([
                'Kneel on the mat with knees hip-width apart',
                'Place hands on your lower back',
                'Gently lean backward',
                'Drop your head back if comfortable',
                'Hold for 30-60 seconds'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Neck Pain',
            'image_url': '/images/camel-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'camel_pose',
            'target_body_parts': 'neck,chest,shoulders'
        },
        {
            'name': "Child's Pose",
            'sanskrit_name': 'Balasana',
            'description': 'Restorative pose that gently stretches the lower back and neck.',
            'benefits': json.dumps(['Relieves neck and lower back pain', 'Stretches hips', 'Calms mind', 'Reduces stress']),
            'instructions': json.dumps([
                'Kneel with big toes touching',
                'Sit back on heels',
                'Fold forward, extend arms',
                'Rest forehead on mat and relax neck',
                'Hold for 1-3 minutes'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Neck Pain',
            'image_url': '/images/child-pose.jpg',
            'duration_seconds': 180,
            'pose_key': 'child_pose',
            'target_body_parts': 'neck,lower_back,hips,shoulders'
        },
        {
            'name': 'Cobra Pose',
            'sanskrit_name': 'Bhujangasana',
            'description': 'Back-bending pose that strengthens the spine and gently stretches the neck.',
            'benefits': json.dumps(['Stretches neck and spine', 'Opens chest', 'Improves posture', 'Relieves stress']),
            'instructions': json.dumps([
                'Lie on stomach, hands under shoulders',
                'Press into hands, lift chest',
                'Keep elbows close to body and look up gently',
                'Hold for 15-30 seconds',
                'Release and repeat 3 times'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Neck Pain',
            'image_url': '/images/cobra-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'cobra_pose',
            'target_body_parts': 'neck,lower_back,chest,shoulders'
        },
        
        # Back Pain
        {
            'name': 'Cat-Cow Pose',
            'sanskrit_name': 'Marjaryasana-Bitilasana',
            'description': 'Gentle flowing movement between arching and rounding the spine.',
            'benefits': json.dumps(['Stretches spine', 'Relieves back tension', 'Improves flexibility', 'Massages internal organs']),
            'instructions': json.dumps([
                'Start on hands and knees',
                'Inhale, arch back, lift head (Cow)',
                'Exhale, round back, tuck chin (Cat)',
                'Flow between poses smoothly',
                'Repeat 10-15 times'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/cat-cow.jpg',
            'duration_seconds': 180,
            'pose_key': 'cat_cow',
            'target_body_parts': 'spine,back,abdomen'
        },
        {
            'name': 'Cobra Pose',
            'sanskrit_name': 'Bhujangasana',
            'description': 'Back-bending pose that strengthens the spine and gently stretches the back.',
            'benefits': json.dumps(['Strengthens spine', 'Relieves lower back pain', 'Improves posture', 'Opens chest']),
            'instructions': json.dumps([
                'Lie on stomach, hands under shoulders',
                'Press into hands, lift chest',
                'Keep elbows close to body and look up gently',
                'Hold for 15-30 seconds',
                'Release and repeat 3 times'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/cobra-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'cobra_pose',
            'target_body_parts': 'lower_back,spine,chest'
        },
        {
            'name': 'Plow Pose',
            'sanskrit_name': 'Halasana',
            'description': 'Inverted pose that provides a deep stretch to the entire spine.',
            'benefits': json.dumps(['Stretches spine and back muscles', 'Relieves backache', 'Calms the brain', 'Stimulates thyroid']),
            'instructions': json.dumps([
                'Lie on your back with arms beside you',
                'Lift your legs and hips off the floor',
                'Bring your legs over your head until toes touch the floor behind you',
                'Support your lower back with your hands',
                'Hold for 30-60 seconds, then roll down slowly'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/halasana.jpg',
            'duration_seconds': 60,
            'pose_key': 'halasana',
            'target_body_parts': 'upper_back,neck,spine'
        },
        {
            'name': 'Seated Forward Bend',
            'sanskrit_name': 'Paschimottanasana',
            'description': 'Classic forward bend that profoundly stretches the back of the body.',
            'benefits': json.dumps(['Stretches lower back', 'Relieves stress', 'Stretches hamstrings', 'Soothes headache']),
            'instructions': json.dumps([
                'Sit on the floor with legs extended forward',
                'Inhale and lengthen your spine',
                'Exhale and hinge forward from your hips',
                'Reach for your shins, ankles, or feet',
                'Hold for 1-3 minutes while breathing deeply'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/paschimottanasana.jpg',
            'duration_seconds': 120,
            'pose_key': 'paschimottanasana',
            'target_body_parts': 'lower_back,hamstrings,spine'
        },
        {
            'name': 'Pigeon Pose',
            'sanskrit_name': 'Eka Pada Rajakapotasana',
            'description': 'Deep hip opener that also relieves tension in the lower back.',
            'benefits': json.dumps(['Relieves lower back pain', 'Releases hip tension', 'Increases hip flexibility', 'Calms the mind']),
            'instructions': json.dumps([
                'Start from Downward Dog',
                'Bring right knee forward behind right wrist',
                'Extend left leg straight back',
                'Square your hips to the front',
                'Fold forward over your front leg or stay upright',
                'Hold for 1-2 minutes, then switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/pigeon-pose.jpg',
            'duration_seconds': 180,
            'pose_key': 'pigeon_pose',
            'target_body_parts': 'lower_back,hips,glutes'
        },
        {
            'name': 'Triangle Pose',
            'sanskrit_name': 'Trikonasana',
            'description': 'Standing pose that stretches the sides of the body and strengthens the back.',
            'benefits': json.dumps(['Relieves backache', 'Stretches the whole back', 'Strengthens legs', 'Opens chest']),
            'instructions': json.dumps([
                'Stand with feet wide apart',
                'Turn right foot out 90 degrees',
                'Extend arms parallel to the floor',
                'Hinge at the right hip and reach right arm down, left arm up',
                'Look up toward your left thumb',
                'Hold for 30-60 seconds, then switch sides'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Back Pain',
            'image_url': '/images/triangle-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'triangle_pose',
            'target_body_parts': 'back,sides,legs'
        },
        
        # Shoulder Pain
        {
            'name': 'Crescent Low Lunge',
            'sanskrit_name': 'Anjaneyasana',
            'description': 'A deep lunge that stretches the hip flexors while actively opening the chest and shoulders.',
            'benefits': json.dumps(['Opens chest and shoulders', 'Stretches hip flexors', 'Builds core strength', 'Improves balance']),
            'instructions': json.dumps([
                'From Downward Dog, step one foot forward between your hands',
                'Lower your back knee to the floor',
                'Sweep your arms up overhead, lifting the chest',
                'Draw your shoulders down your back and gently arch your upper back',
                'Hold for 30-60 seconds, then switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Shoulder Pain',
            'image_url': '/images/anjaneyasana.jpg',
            'duration_seconds': 120,
            'pose_key': 'anjaneyasana',
            'target_body_parts': 'shoulders,chest,hips'
        },
        {
            'name': 'Cow Face Pose',
            'sanskrit_name': 'Gomukhasana',
            'description': 'A seated posture that provides a deep stretch for the shoulders, armpits, and chest.',
            'benefits': json.dumps(['Deep shoulder stretch', 'Opens chest', 'Increases shoulder mobility', 'Relieves upper back tension']),
            'instructions': json.dumps([
                'Sit comfortably, ideally crossing one leg over the other',
                'Bring your right arm straight up, then bend the elbow so the hand drops down your back',
                'Bring your left arm behind your back from below and reach up',
                'Try to clasp hands if possible, or use a strap',
                'Keep your chest lifted and hold for 30-60 seconds, then switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Shoulder Pain',
            'image_url': '/images/cow-face.jpg',
            'duration_seconds': 120,
            'pose_key': 'cow_face',
            'target_body_parts': 'shoulders,chest,arms'
        },
        {
            'name': 'Locust Pose',
            'sanskrit_name': 'Salabhasana',
            'description': 'A back-bending pose that strengthens the entire back and opens the chest and shoulders.',
            'benefits': json.dumps(['Strengthens back muscles', 'Opens chest and shoulders', 'Improves posture', 'Relieves stress']),
            'instructions': json.dumps([
                'Lie on your stomach with arms alongside your body, palms down',
                'Inhale and lift your head, chest, arms, and legs off the floor',
                'Reach your arms actively back, squeezing your shoulder blades together',
                'Gaze forward and slightly down',
                'Hold for 30 seconds, then release'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Shoulder Pain',
            'image_url': '/images/locust.jpg',
            'duration_seconds': 60,
            'pose_key': 'locust',
            'target_body_parts': 'back,shoulders,chest'
        },
        
        # Knee Pain
        {
            'name': 'Chair Pose',
            'sanskrit_name': 'Utkatasana',
            'description': 'Strengthening pose for legs and knees with controlled squat.',
            'benefits': json.dumps(['Strengthens knees', 'Tones legs', 'Builds stability', 'Improves balance']),
            'instructions': json.dumps([
                'Stand with feet together',
                'Bend knees, lower hips',
                'Raise arms overhead',
                'Keep weight in heels',
                'Hold for 30-60 seconds'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Knee Pain',
            'image_url': '/images/chair-pose.jpg',
            'duration_seconds': 90,
            'pose_key': 'chair_pose',
            'target_body_parts': 'knees,legs,core'
        },
        {
            'name': "Child's Pose",
            'sanskrit_name': 'Balasana',
            'description': 'Restorative pose that gently stretches the lower back, hips, and knees.',
            'benefits': json.dumps(['Relieves lower back pain', 'Gently stretches knees', 'Calms mind', 'Reduces stress']),
            'instructions': json.dumps([
                'Kneel with big toes touching',
                'Sit back on heels (use a blanket behind knees for support if needed)',
                'Fold forward, extend arms',
                'Rest forehead on mat',
                'Hold for 1-3 minutes'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Knee Pain',
            'image_url': '/images/child-pose.jpg',
            'duration_seconds': 180,
            'pose_key': 'child_pose',
            'target_body_parts': 'knees,lower_back,hips'
        },
        {
            'name': 'Warrior II',
            'sanskrit_name': 'Virabhadrasana II',
            'description': 'Strengthening pose that builds leg stability and opens hips.',
            'benefits': json.dumps(['Builds leg strength', 'Opens hips', 'Improves stamina', 'Enhances focus']),
            'instructions': json.dumps([
                'Step feet wide apart',
                'Turn right foot out 90 degrees',
                'Bend right knee over ankle',
                'Extend arms to sides',
                'Hold for 30 seconds, switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Knee Pain',
            'image_url': '/images/warrior-ii.jpg',
            'duration_seconds': 120,
            'pose_key': 'warrior_ii',
            'target_body_parts': 'legs,knees,hips,shoulders'
        },
        
        # Stress Relief
        {
            'name': 'Boat Pose',
            'sanskrit_name': 'Navasana',
            'description': 'A core-strengthening pose that builds focus and resilience against stress.',
            'benefits': json.dumps(['Builds core strength', 'Relieves stress', 'Improves focus', 'Stimulates digestion']),
            'instructions': json.dumps([
                'Sit with knees bent, feet flat on the floor',
                'Lean back slightly, keeping spine straight',
                'Lift feet off the floor, bringing shins parallel to the mat',
                'Extend arms forward, parallel to the floor',
                'Hold for 30-60 seconds, breathing deeply'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Stress Relief',
            'image_url': '/images/boat-pose.jpg',
            'duration_seconds': 60,
            'pose_key': 'boat_pose',
            'target_body_parts': 'core,hip_flexors,spine'
        },
        {
            'name': 'Bridge Pose',
            'sanskrit_name': 'Setu Bandhasana',
            'description': 'A gentle backbend that opens the chest and calms the nervous system.',
            'benefits': json.dumps(['Calms the brain', 'Alleviates stress', 'Stretches the chest, neck, and spine', 'Reduces anxiety']),
            'instructions': json.dumps([
                'Lie on your back with knees bent and feet hip-width apart',
                'Press your arms into the floor and lift your hips toward the ceiling',
                'Roll your shoulders under your body',
                'Keep your neck neutral and breathe smoothly',
                'Hold for 30-60 seconds, then release slowly'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'Stress Relief',
            'image_url': '/images/bridge-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'bridge_pose',
            'target_body_parts': 'chest,neck,spine,hips'
        },
        {
            'name': "Child's Pose",
            'sanskrit_name': 'Balasana',
            'description': 'A profoundly restful pose that quiets the mind and relieves tension.',
            'benefits': json.dumps(['Quickly calms the mind', 'Reduces stress and anxiety', 'Soothes the nervous system', 'Releases lower back tension']),
            'instructions': json.dumps([
                'Kneel on the floor, toes together, knees apart',
                'Sit back on your heels',
                'Exhale and fold forward, resting your torso between your thighs',
                'Extend arms forward or rest them alongside your body',
                'Hold for 1-5 minutes, focusing on your breath'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Stress Relief',
            'image_url': '/images/child-pose.jpg',
            'duration_seconds': 300,
            'pose_key': 'child_pose',
            'target_body_parts': 'mind,lower_back,hips'
        },
        {
            'name': 'Corpse Pose',
            'sanskrit_name': 'Savasana',
            'description': 'Deep relaxation pose to calm the mind and completely release tension.',
            'benefits': json.dumps(['Deep relaxation', 'Reduces stress', 'Calms mind', 'Balances the nervous system']),
            'instructions': json.dumps([
                'Lie flat on back',
                'Arms at sides, palms up',
                'Close eyes and relax all muscles',
                'Breathe naturally and release all effort',
                'Stay for 5-10 minutes'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'Stress Relief',
            'image_url': '/images/corpse-pose.jpg',
            'duration_seconds': 300,
            'pose_key': 'corpse_pose',
            'target_body_parts': 'full_body'
        },
        
        # General Wellness
        {
            'name': 'Downward Dog',
            'sanskrit_name': 'Adho Mukha Svanasana',
            'description': 'Full-body stretch that strengthens and energizes.',
            'benefits': json.dumps(['Stretches full body', 'Builds strength', 'Energizes mind', 'Improves circulation']),
            'instructions': json.dumps([
                'Start on hands and knees',
                'Lift hips up and back',
                'Form inverted V shape',
                'Press heels toward mat',
                'Hold for 30-60 seconds'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/downward-dog.jpg',
            'duration_seconds': 90,
            'pose_key': 'downward_dog',
            'target_body_parts': 'full_body'
        },
        {
            'name': 'Goddess Pose',
            'sanskrit_name': 'Utkata Konasana',
            'description': 'A powerful standing squat that strengthens the lower body and opens the hips.',
            'benefits': json.dumps(['Strengthens lower body', 'Opens hips and chest', 'Builds heat', 'Empowers the mind']),
            'instructions': json.dumps([
                'Step feet wide apart',
                'Turn toes outward',
                'Bend knees deeply directly over ankles',
                'Bend elbows to 90 degrees with fingers spread',
                'Hold for 30-60 seconds'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/goddess-pose.jpg',
            'duration_seconds': 90,
            'pose_key': 'goddess_pose',
            'target_body_parts': 'legs,hips,core'
        },
        {
            'name': "Dancer's Pose",
            'sanskrit_name': 'Natarajasana',
            'description': 'A graceful balancing pose that develops focus, balance, and flexibility.',
            'benefits': json.dumps(['Improves balance', 'Stretches the whole front body', 'Strengthens legs', 'Builds intense focus']),
            'instructions': json.dumps([
                'Stand on your right leg',
                'Bend your left knee and catch your left foot with your left hand',
                'Reach your right arm forward and up',
                'Slowly kick your left foot into your hand while leaning forward slightly',
                'Hold for 30 seconds, then switch sides'
            ]),
            'difficulty_level': 'advanced',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/natarajasana.jpg',
            'duration_seconds': 120,
            'pose_key': 'natarajasana',
            'target_body_parts': 'legs,core,chest,balance'
        },
        {
            'name': 'Pyramid Pose',
            'sanskrit_name': 'Parsvottanasana',
            'description': 'An intense side stretch that lengthens the spine and hamstrings.',
            'benefits': json.dumps(['Deep hamstring stretch', 'Improves balance', 'Strengthens legs', 'Calms the mind']),
            'instructions': json.dumps([
                'Step your right foot forward and left foot back about 3 feet',
                'Keep both legs straight and hips squared forward',
                'Hinge at your hips and fold over your right leg',
                'Rest hands on your shin, foot, or the floor',
                'Hold for 30-60 seconds, then switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/parsvottanasana.jpg',
            'duration_seconds': 120,
            'pose_key': 'parsvottanasana',
            'target_body_parts': 'hamstrings,spine,legs'
        },
        {
            'name': 'Plank Pose',
            'sanskrit_name': 'Phalakasana',
            'description': 'Core-strengthening pose that builds total body strength.',
            'benefits': json.dumps(['Strengthens core', 'Builds arm strength', 'Tones legs', 'Improves posture']),
            'instructions': json.dumps([
                'Start in push-up position',
                'Align wrists under shoulders',
                'Engage core, straight line from head to heels',
                'Hold for 30-60 seconds',
                'Rest and repeat'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/plank-pose.jpg',
            'duration_seconds': 90,
            'pose_key': 'plank',
            'target_body_parts': 'core,arms,legs'
        },
        {
            'name': 'Standing Mountain Pose',
            'sanskrit_name': 'Tadasana',
            'description': 'Foundation standing pose that improves posture and alignment.',
            'benefits': json.dumps(['Improves posture', 'Builds awareness', 'Strengthens legs', 'Grounds energy']),
            'instructions': json.dumps([
                'Stand with feet together',
                'Ground through all four corners of your feet',
                'Engage thighs, lift chest',
                'Relax shoulders down',
                'Hold for 30-60 seconds'
            ]),
            'difficulty_level': 'beginner',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/mountain-pose.jpg',
            'duration_seconds': 60,
            'pose_key': 'mountain_pose',
            'target_body_parts': 'full_body'
        },
        {
            'name': 'Tree Pose',
            'sanskrit_name': 'Vrksasana',
            'description': 'Balancing pose that improves focus and leg strength.',
            'benefits': json.dumps(['Improves balance', 'Strengthens legs', 'Builds focus', 'Opens hips']),
            'instructions': json.dumps([
                'Stand on left leg',
                'Place right foot on inner thigh or calf (avoid the knee)',
                'Bring hands to heart center',
                'Find a focal point',
                'Hold for 30 seconds, switch sides'
            ]),
            'difficulty_level': 'intermediate',
            'pain_category_id': 'General Wellness',
            'image_url': '/images/tree-pose.jpg',
            'duration_seconds': 120,
            'pose_key': 'tree_pose',
            'target_body_parts': 'legs,core,balance'
        }
    ]
    
    # Create exercises
    for ex_data in exercises_data:
        # Get category ID
        cat_name = ex_data.pop('pain_category_id')
        ex_data['pain_category_id'] = category_map.get(cat_name)
        
        # Check if exercise exists in this category
        existing = Exercise.query.filter_by(
            name=ex_data['name'],
            pain_category_id=ex_data['pain_category_id']
        ).first()
        if not existing:
            exercise = Exercise(**ex_data)
            db.session.add(exercise)
            print(f"  Created exercise: {ex_data['name']}")
        else:
            print(f"  Exercise exists: {ex_data['name']}")
    
    db.session.commit()
    print("\nDatabase seeding completed!")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_database()

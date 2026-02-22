import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

# Load parsed bookmarks
with open('fitness_bookmarks.json', 'r') as f:
    bookmarks = json.load(f)

# AI Analysis Data
ANALYSIS = {
    "irregular sleep is just as bad as getting less sleep - YouTube": {
        "type": "Article", "rating": "7", "notes": "Consistency is king. Circadian rhythm disruption is as damaging as deprivation.",
        "summary": "Go to bed at the same time. This video explains why your weekend sleep-ins are actually jet lag. Read this to fix your rhythm."
    },
    "6 Steps to Hack Your Health in 2026 | Dr. Ezekiel Emanuel": {
        "type": "Article", "rating": "7", "notes": "Preventive checklist. Screening, diet, and sleep.",
        "summary": "The longevity checklist. A simple, actionable guide to not dying early. Read this for your annual health audit."
    },
    "Meditation risks, safety, goals, methods | Vividness": {
        "type": "Article", "rating": "8", "notes": "The dark side of meditation. Navigating the 'dark night of the soul'.",
        "summary": "It's not all peace and love. A safety manual for advanced meditation practice. Read this if you're getting serious about the cushion."
    },
    "Getting Jacked is Simple": {
        "type": "Article", "rating": "7", "notes": "Hypertrophy basics. Progressive overload + Caloric surplus.",
        "summary": "Stop overcomplicating it. This article strips away the bro-science to reveal the simple math of muscle growth. Read this to start growing."
    },
    "Thin": {
        "type": "Essay", "rating": "7", "notes": "Cultural analysis of the desire for thinness. The intersection of aesthetics and morality.",
        "summary": "Why do we want to be small? An essay on the cultural weight of weight. Read this to unpack your body image focus."
    },
    "HOW TO FIX YOUR LIFE: Full Self Improvement Guide": {
        "type": "Article", "rating": "8", "notes": "Comprehensive protocol. Sleep, diet, exercise, and mental health as a system.",
        "summary": "The total overhaul. A step-by-step guide to fixing your biological machinery. Read this if you feel like a broken robot."
    },
    "Why Your Sleep Habits Aren't Healthy": {
        "type": "Article", "rating": "6", "notes": "Sleep hygiene 101. Screens, temperature, and caffeine.",
        "summary": "The basics of slumber. A refresher on why you're tired all the time. Read this if you drink coffee at 5 PM."
    },
    "Fat | Google NotebookLM": {
        "type": "Article", "rating": "6", "notes": "AI-synthesized notes on fat metabolism.",
        "summary": "What is fat? A deep dive into the biology of adipose tissue. Read this to understand what you're trying to lose."
    },
    "Blueprint Protocol": {
        "type": "Article", "rating": "8", "notes": "Bryan Johnson's extreme longevity routine. The gamification of biological age.",
        "summary": "The most measured man in the world. An outline of the Blueprint protocol. Read this for extreme inspiration (or horror)."
    },
    "After 8 years in the gym, here's every fitness tip I could come up with:": {
        "type": "Article", "rating": "8", "notes": "Experience-based wisdom. Consistency > Intensity. Form > Weight.",
        "summary": "Bro-wisdom distilled. 8 years of mistakes compressed into one thread. Read this to save yourself a decade of bad lifting."
    },
    "Up All Night | The New Yorker": {
        "type": "Article", "rating": "9", "notes": "The history and science of insomnia. The cultural anxiety around sleep.",
        "summary": "The nightmare of wakefulness. The New Yorker explores why we can't sleep. Read this if you're reading this at 3 AM."
    },
    "The Last Conversation You’ll Need to Have About Eating Right": {
        "type": "Article", "rating": "8", "notes": "Pollan-esque simplicity. Eat real food. Mostly plants. Not too much.",
        "summary": "Nutrition is solved. This article cuts through the diet wars with simple, un-gameable advice. Read this and never diet again."
    },
    "Why you shouldn't exercise to lose weight, explained with 60+ studies - Vox": {
        "type": "Article", "rating": "8", "notes": "Exercise is for health; diet is for weight. The constraint of total energy expenditure.",
        "summary": "You can't outrun a bad diet. Vox explains the science of why the gym won't make you skinny. Read this to adjust your expectations."
    },
    "How to Become a Morning Exercise Person - The New York Times": {
        "type": "Article", "rating": "7", "notes": "Habit stacking. Preparation (clothes out the night before) and reward bundling.",
        "summary": "Own the morning. Practical tips to drag yourself out of bed. Read this if you snooze your alarm 5 times."
    },
    "Could Ice Cream Possibly Be Good for You? - The Atlantic": {
        "type": "Article", "rating": "7", "notes": "The 'dairy fat paradox'. Identifying nutritional blind spots.",
        "summary": "The best news you've heard all day. Investigating the mysterious health benefits of dairy fat. Read this while eating a sundae."
    },
    "Fat, Sugar, Salt ... You’ve Been Thinking About Food All Wrong | WIRED": {
        "type": "Article", "rating": "9", "notes": "The 'bliss point'. How processed food is engineered to bypass satiety mechanisms.",
        "summary": "You are being hacked. precise engineering of junk food addiction. Read this to understand why you can't eat just one."
    },
    "Will Ozempic Change How We Think About Being Fat and Being Thin? | The New Yorker": {
        "type": "Article", "rating": "9", "notes": "GLP-1 agonists and the death of the 'willpower' model of obesity.",
        "summary": "The end of the diet. The New Yorker analyzes the Ozempic revolution. Read this to understand the future of bodies."
    },
    "I lost 9 kg and got rid of my big stubborn belly in less than 6 months. Here’s how I achieved my 2023 resolution": {
        "type": "Article", "rating": "6", "notes": "Case study. CICO, protein, and resistance training.",
        "summary": "It's possible. A straightforward success story to prove the basics work. Read this for motivation."
    },
    "Fat loss hacks I know at 44 that I wish I knew at 24:": {
        "type": "Article", "rating": "7", "notes": "Age-adjusted fitness. Protein prioritization and recovery focus.",
        "summary": "Fitness after 40. How to stay lean when your metabolism slows down. Read this if you're not 21 anymore."
    },
    "Best in Class Life Improvement — LessWrong": {
        "type": "Essay", "rating": "9", "notes": "Compendium of optimal protocols. From sleep to lighting to ergonomics.",
        "summary": "The bible of optimization. LessWrong compiles the best interventions for everything. Read this to fix your entire life stack."
    },
    "Rational Health Optimization — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Evidence-based supplementation and lifestyle tweaks. Pareto principle applied to health.",
        "summary": "Health for nerds. A data-driven guide to keeping your meat-suit running. Read this to stop wasting money on placebo supplements."
    },
    "How I Lost 100 Pounds Using TDT — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Theory driven weight loss. Psychological frameworks for adherence.",
        "summary": "The psychology of shedding weight. A deep dive into the mental shifts required to lose 100lbs. Read this for the mind game of weight loss."
    },
    "Akrasia Tactics Review — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Duplicate entry. Productivity tactics.",
        "summary": "How to actually do things. A comprehensive review of every productivity hack that works. Read this to defeat procrastination."
    },
    "Notes on Fitness — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "The rationalist guide to lifting. Minimum effective dose for hypertrophy.",
        "summary": "Lifting for smart people. How to get strong without living in the gym. Read this for the most efficient path to gains."
    },
    "Travels": {
        "type": "Article", "rating": "6", "notes": "Fitness maintenance while traveling. Bodyweight routines and step counts.",
        "summary": "Don't lose your gains on vacation. How to stay fit on the road. Read this before your next trip."
    },
    "Toolkit for Sleep": {
        "type": "Article", "rating": "9", "notes": "Huberman Lab protocols. Light viewing, temperature, caffeine timing.",
        "summary": "The master class on sleep. Use these tools to engineer the perfect night's rest. Read this to wake up energized."
    },
    "The Science & Use of Cold Exposure for Health & Performance": {
        "type": "Article", "rating": "8", "notes": "Cold plunging. Dopamine regulation and metabolic effects.",
        "summary": "Get cold. Why freezing yourself is the hottest health trend. Read this to understand the dopamine benefits of ice baths."
    },
    "My Effortless Weightloss Story: A Quick Runthrough": {
        "type": "Article", "rating": "7", "notes": "Intermittent fasting focus. Reducing decision fatigue around food.",
        "summary": "Weight loss on autopilot. How to structure your life so you lose weight by default. Read this if you hate counting calories."
    },
    "r/loseit wiki": {
        "type": "Article", "rating": "9", "notes": "The definitive guide to CICO. No-nonsense physics of weight loss.",
        "summary": "The laws of thermodynamics applied to your body. The single best resource on the internet for weight loss. Read this to stop guessing."
    },
    "r/loseit qsg": {
        "type": "Article", "rating": "8", "notes": "Quick Start Guide. Calculate TDEE, track calories, waiting.",
        "summary": "Start here. A distillation of the wiki into a step-by-step plan. Read this to start losing weight today."
    },
    "What to do if you DON’T like to exercise: | Nerd Fitness": {
        "type": "Article", "rating": "8", "notes": "Gamification. reframing exercise as 'movement' or 'play'. Finding your activity.",
        "summary": "You don't have to run. How to find a movement practice you actually enjoy. Read this if you hate the gym."
    },
    "The Fitness Wiki": {
        "type": "Article", "rating": "9", "notes": "The bible of beginner lifting programs. Starting Strength, GZCLP, etc.",
        "summary": "The roadmap to strength. The cumulative wisdom of the internet's fittest people. Read this to pick a program that works."
    },
    "Conquering Insomnia CBT-I Program - CBT-I": {
        "type": "Article", "rating": "9", "notes": "Gold standard treatment. Sleep restriction therapy and stimulus control.",
        "summary": "The cure for insomnia. Forget pills; this psychological protocol actually retrains your brain to sleep. Read this if you're desperate."
    },
    "All The Basics Workout": {
        "type": "Article", "rating": "7", "notes": "Foundational movement patterns. Squat, Hinge, Push, Pull, Carry.",
        "summary": "Cover your bases. A simple routine that hits every muscle group. Read this for a foolproof workout."
    }
}

def create_notion_page(data):
    # Lookup analysis data
    analysis = ANALYSIS.get(data['title'], {
        "type": "Article", "rating": "5", "notes": "Synced from Raindrop.", "summary": "No summary available."
    })
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": data["title"]}}]
            },
            "URL": {
                "url": data["url"]
            },
            "State": {
                "status": {"name": "AI-Read"}
            },
            "Type": {
                "select": {"name": analysis["type"]}
            },
            "Tags": {
                "multi_select": [{"name": "Fitness"}]
            },
            "Notes": {
                "rich_text": [{"text": {"content": analysis["notes"]}}]
            },
            "Rating": {
                "select": {"name": analysis["rating"]}
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Why should I bother reading this article?"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": analysis["summary"]}}]
                }
            }
        ]
    }

    if data.get("highlights"):
        payload["children"].append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Highlights"}}]
            }
        })
        for highlight in data["highlights"]:
            if highlight:
                payload["children"].append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": highlight[:2000]}}]
                    }
                })
    
    response = requests.post(f"{NOTION_API_BASE}/pages", headers=headers, json=payload)
    if not response.ok:
        print(f"Failed to create Notion page for {data['title']}: {response.text}")
    else:
        print(f"Successfully created Notion page for: {data['title']}")

if __name__ == "__main__":
    for item in bookmarks:
        create_notion_page(item)

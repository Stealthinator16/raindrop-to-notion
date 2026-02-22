import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_BASE = "https://api.notion.com/v1"

# Load parsed bookmarks
with open('mental_fitness_bookmarks.json', 'r') as f:
    bookmarks = json.load(f)

# AI Analysis Data
ANALYSIS = {
    "How Meditation Works & Science-Based Effective Meditations | Huberman Lab Podcast #96": {
        "type": "Article", "rating": "9", "notes": "Deep dive into the neuroscience of focus and relaxation. Protocol-based.",
        "summary": "This isn't just 'woo'. Huberman breaks down the biological mechanisms of meditation. Read this to understand how to manually toggle your nervous system."
    },
    "How to do the jhanas": {
        "type": "Article", "rating": "8", "notes": "Technical manual for entering altered states of consciousness without drugs.",
        "summary": "Meditation on steroids. A practical guide to accessing the 'jhanas'—states of intense absorption and bliss. Read this if mindfulness feels too boring."
    },
    "Manufacturing Bliss—Asterisk": {
        "type": "Essay", "rating": "8", "notes": "Critique of the wellness industry and the engineering of happiness.",
        "summary": "Can we engineer joy? This essay explores the philosophical implications of 'manufacturing bliss'. Read this to question the pursuit of happiness."
    },
    "Explore More: A Bag of Tricks to Keep Your Life on the Rails — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Application of 'explore vs exploit' algorithms to personal life.",
        "summary": "You're getting stuck in local optimums. This rationalist guide argues for more randomness and exploration in life. Read this to break out of your rut."
    },
    "ADHD is not a disorder.": {
        "type": "Article", "rating": "7", "notes": "The 'hunter vs farmer' hypothesis. Reframing neurodivergence as an evolutionary adaptation.",
        "summary": "You aren't broken; you're just in the wrong century. This argument reframes ADHD as a 'hunter' trait in a 'farmer' world. Read this for a confidence boost."
    },
    "(1/8) Yesterday I said it was wild how many talented people struggle to sell themselves during interviews": {
        "type": "Article", "rating": "7", "notes": "Interview strategy. The gap between competence and the ability to signal it.",
        "summary": "Don't be humble. This thread explains why smart people fail interviews and how to fix it. Read this before your next job hunt."
    },
    "Building mental immunity against depression and anxiety": {
        "type": "Article", "rating": "8", "notes": "CBT and Stoic techniques for psychological resilience.",
        "summary": "Vaccinate your mind. This guide combines Stoicism and psychology to build a 'mental immune system'. Read this to become antifragile."
    },
    "Akrasia Tactics Review — LessWrong": {
        "type": "Essay", "rating": "9", "notes": "Battle-tested anti-procrastination techniques. 'Eat the frog' meets game theory.",
        "summary": "How to actually do things. A comprehensive review of every productivity hack that works. Read this to defeat procrastination."
    },
    "A Comprehensive Manual of Abhidhamma: The Abhidhammattha Sangaha of Acariya Anuruddha": {
        "type": "Article", "rating": "9", "notes": "The atomic theory of the mind. Foundational text of Buddhist psychology.",
        "summary": "The periodic table of consciousness. This is a deep dive into the 'Abhidhamma', the ancient system that maps every state of mind. Read this if into hardcore psychology."
    },
    "The Secret Power of ‘Read It Later’ Apps": {
        "type": "Article", "rating": "7", "notes": "Knowledge management. Separation of discovery (collecting) and consumption (reading).",
        "summary": "Stop tab hoarding. Tiago Forte explains why you need a 'holding tank' for information. Read this to save your browser RAM and your sanity."
    },
    "How Millennials Became The Burnout Generation": {
        "type": "Article", "rating": "9", "notes": "Viral Buzzfeed essay. 'Errand paralysis' and the structural causes of exhaustion.",
        "summary": "It's not just you. This viral essay explains why simple errands feel impossible for an entire generation. Read this to feel seen."
    },
    "How one hour of slow breathing changed my life | Health & wellbeing | The Guardian": {
        "type": "Article", "rating": "8", "notes": "Breathwork as a physiological reset button. Vagus nerve stimulation.",
        "summary": "Just breathe. A skeptic discovers the power of breathwork to cure anxiety. Read this for a free, biological stress hack."
    },
    "How to Prevent Memory Loss - The New York Times": {
        "type": "Article", "rating": "7", "notes": "Standard advice: sleep, diet, exercise, and novelty.",
        "summary": "Use it or lose it. The NYT summarizes the evidence-based ways to keep your brain sharp. Read this to protect your future self."
    },
    "The Daily Habits of Happiness Experts | TIME": {
        "type": "Article", "rating": "7", "notes": "Positive psychology interventions. Gratitude, connection, and movement.",
        "summary": "What do happy people do? Experts reveal their own daily routines. Read this for actionable, science-backed habits."
    },
    "Memory loss: Expert advice for improving memory and concentration - Vox": {
        "type": "Article", "rating": "7", "notes": "Focus and attention management as the gateway to memory.",
        "summary": "You don't have a bad memory; you have bad attention. Vox explains how to improve recall by improving focus. Read this to stop forgetting names."
    },
    "Your bad attitude can make you happier - The Atlantic": {
        "type": "Article", "rating": "7", "notes": "Defensive pessimism. The bright side of cynicism.",
        "summary": "Stop forcing a smile. This article argues that 'negative visualization' is a powerful happiness tool. Read this if you hate toxic positivity."
    },
    "How to Find More Joy in Your Day, According to Author Katherine May - The New York Times": {
        "type": "Article", "rating": "8", "notes": "Enchantment. Noticing the magic in the mundane.",
        "summary": "Re-enchant your life. Katherine May argues that awe is a skill you can practice. Read this to see the world with fresh eyes."
    },
    "How to forgive yourself | Psyche Guides": {
        "type": "Article", "rating": "8", "notes": "Self-compassion vs. self-esteem. The mechanism of guilt release.",
        "summary": "Let it go. A psychological guide to recovering from your own mistakes. Read this to stop the 3 AM cringe sessions."
    },
    "Why Everyone Feels Like They’re Faking It | The New Yorker": {
        "type": "Article", "rating": "8", "notes": "Cultural history of Impostor Syndrome. Is it individual pathology or systemic exclusion?",
        "summary": "You aren't a fraud. The New Yorker deconstructs 'Impostor Syndrome'. Read this to understand why you feel unqualified."
    },
    "Why Is LED Light So Bad? | The Strategist": {
        "type": "Article", "rating": "7", "notes": "Circadian biology. The impact of blue light spectrum on health.",
        "summary": "Your lightbulbs are making you sick. An investigation into why modern lighting feels so harsh. Read this to fix your sleep hygiene."
    },
    "Since when is philosophy a branch of the self-help industry? | Aeon Essays": {
        "type": "Essay", "rating": "8", "notes": "Critique of 'McStoicism'. Philosophy as a way of life vs. a productivity hack.",
        "summary": "Stoicism isn't for productivity. Aeon critiques the modern commodification of ancient wisdom. Read this to rescue philosophy from the life hackers."
    },
    "How I rewired my brain in six weeks": {
        "type": "Article", "rating": "7", "notes": "Personal experiment with neuroplasticity. Meditation and cognitive training.",
        "summary": "Brain training IRL. A journalist documents an attempt to upgrade their mind. Read this for inspiration on neuroplasticity."
    },
    "Bronze Age Pervert's Guide to Philosophy": {
        "type": "Article", "rating": "6", "notes": "Analysis of the BAP phenomenon. The intersection of bodybuilding, philosophy, and right-wing memes.",
        "summary": "The weirdest corner of the internet. A deep dive into the cult of 'Bronze Age Pervert'. Read this to understand the online right."
    },
    "From the pseudo to the forger: the value of faked philosophy | Aeon Essays": {
        "type": "Essay", "rating": "7", "notes": "Authenticity in thought. When is a fake insight still valuable?",
        "summary": "Fake deep? This essay explores the line between profundity and nonsense. Read this to sharpen your BS detector."
    },
    "What we talk about when we talk about giving up | Psychology | The Guardian": {
        "type": "Article", "rating": "8", "notes": "Psychoanalysis of quitting. The sunk cost fallacy vs. grit.",
        "summary": "It's okay to quit. The Guardian explores the psychology of giving up. Read this if you're holding on too long."
    },
    "Is Philosophy Self-Help? | The Point Magazine": {
        "type": "Essay", "rating": "7", "notes": "The therapeutic origin of philosophy. Epicurus and Stoics viewed it as medicine for the soul.",
        "summary": "Therapy for the soul. This essay argues that philosophy was the original self-help. Read this to find comfort in big ideas."
    },
    "Tripping on LSD at the Dolphin Research Lab": {
        "type": "Article", "rating": "9", "notes": "John C. Lilly. The wildest experiment in history. Interspecies communication and psychedelics.",
        "summary": "Dolphins on acid. This is the true story of the most bonkers experiment of the 60s. Read this for pure, historical madness."
    },
    "The Skill You’ve Never Been Taught: How to Think Better": {
        "type": "Article", "rating": "8", "notes": "Metacognition. First principles thinking and mental models.",
        "summary": "Upgrade your OS. A guide to thinking about thinking. Read this to stop running on autopilot."
    },
    "Manufacturing Bliss - Asterisk Magazine": {
        "type": "Essay", "rating": "8", "notes": "Critique of the wellness industry. (Duplicate entry)",
        "summary": "Can we engineer joy? This essay explores the philosophical implications of 'manufacturing bliss'. Read this to question the pursuit of happiness."
    },
    "Book Review: Mastering The Core Teachings Of The Buddha | Slate Star Codex": {
        "type": "Article", "rating": "9", "notes": "Rationalist review of Ingram's 'hardcore dharma'. Enlightenment as a technical problem.",
        "summary": "Buddhism for engineers. Scott Alexander reviews the book that demystifies enlightenment. Read this if you like your spirituality with data."
    },
    "Is Rationalist Self-Improvement Real? — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Skepticism about the effectiveness of 'optimizing' one's life. The 'valley of bad rationality'.",
        "summary": "Does any of this work? A rationalist asks if self-improvement is actually improving anything. Read this for a necessary reality check."
    },
    "I'm 44.": {
        "type": "Article", "rating": "7", "notes": "Mid-life reflection. Acceptance of aging and shifting priorities.",
        "summary": "Getting older, getting wiser. A short, poignant reflection on hitting middle age. Read this to make peace with time."
    },
    "7 habits of highly miserable people:": {
        "type": "Article", "rating": "9", "notes": "Inversion. To be happy, avoid the things that make you miserable (isolation, inactivity, envy).",
        "summary": "How to ruin your life. CGP Grey's guide to misery uses 'inversion' to teach happiness. Read this to know exactly what to avoid."
    },
    "Being a lifelong learner isn’t about taking pride in your knowledge. It's about having the humility to know what you don’t know.": {
        "type": "Article", "rating": "7", "notes": "Adam Grant? Intellectual humility as the core of growth.",
        "summary": "Be humble. This snippet reminds us that learning starts with admitting ignorance. Read this to keep your ego in check."
    },
    "How to get creative (without doing drugs)": {
        "type": "Article", "rating": "7", "notes": "Lateral thinking. Changing context to spark insight.",
        "summary": "Spark your brain. Practical tips for creativity that don't involve microdosing. Read this when you need a new idea."
    },
    "40 things I wish I knew when I was 20": {
        "type": "Article", "rating": "7", "notes": "Life advice listicle. Compound interest, relationships, and risk.",
        "summary": "Wisdom in hindsight. A list of 40 lessons for a well-lived life. Read this to avoid making the same mistakes."
    },
    "Vanity metrics: How to pick better life goals": {
        "type": "Article", "rating": "8", "notes": "Julian Shapiro. Optimize for the right things, not just the measurable ones.",
        "summary": "Stop counting likes. Julian Shapiro argues that we often optimize for 'vanity metrics' in life. Read this to choose better goals."
    },
    "Memorized Rules: How to give your life direction": {
        "type": "Article", "rating": "8", "notes": "Cognitive offloading. Creating heuristics for decision making.",
        "summary": "Rules to live by. How to create personal heuristics that save you brainpower. Read this to automate your decisions."
    },
    "How to figure out what to do with your life": {
        "type": "Article", "rating": "9", "notes": "Life strategy. Minimizing regret and maximizing optionality.",
        "summary": "The ultimate guide to life planning. Julian Shapiro breaks down how to choose a path. Read this if you feel lost."
    },
    "Willpower Hax #487: Execute by Default — LessWrong": {
        "type": "Essay", "rating": "8", "notes": "Monoidealism. Using momentum to bypass decision fatigue.",
        "summary": "Don't think, just do. This trick uses 'monoidealism' to bypass willpower battles. Read this to become an execution machine."
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
                "multi_select": [{"name": "Mental Fitness"}]
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

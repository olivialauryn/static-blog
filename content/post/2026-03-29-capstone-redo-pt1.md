---
title: "Capstone Revisited Pt1"
date: 2026-03-29T10:44:59-04:00
draft: false
tags: ["AI", "Claude", "Automation", "Python", "Kaggle"]
---

# I Redid My 2020 College Capstone With AI — Here's What Changed

In 2020, I spent my senior year of college building a machine learning model for my capstone project. Inspired by new (at the time) advances in self-driving cars, the goal to train a convolutional neural network (CNN) to detect obstacles in road images. Then prove that biased training data made it worse. It took months of grinding through TensorFlow documentation, manually hunting for images, and writing code I didn't fully understand yet.

In 2026, I redid the entire thing in a single conversation with Claude.

This post is about what that experience revealed — not just about how much AI tooling has improved, but about what it means to actually understand a project versus just completing one.

---

## The original project

Read about my original capstone at the blog posts here:
[pt1](https://osnowden.com/post/2020-capstone-pt1/)
[pt2](https://osnowden.com/post/2020-capstone-pt2/)

Self-driving cars use neural networks to detect obstacles — pedestrians, cyclists, vehicles — and if those networks are trained on biased data, they perform poorly in conditions they've never seen. I wanted to demonstrate this experimentally using a model I built myself.

The 2020 version had real limitations. My dataset was only 200 images since I scraped manually from a dashcam livestream website and a Kaggle dataset. My CNN was copied largely from TensorFlow tutorials. The code worked, sort of. Testing accuracy hovered between 72–80%, which I had to be happy with given how small my dataset was.

One of my utility scripts had a bug I didn't catch until years later: `i=+1` always set the counter to 1 instead of incrementing it. Small, but the kind of thing that erodes confidence in your own results.

---

## What I brought to Claude in 2026

I uploaded everything: two blog posts I'd written explaining the project, the academic paper draft, and the Python scripts I originally used to edit images. Then I described what I wanted: redo the experiment, modernize the code, understand it better this time.

### The code audit

Claude read through my original scripts and immediately flagged things I'd missed. The `i=+1` bug. A typo in `RandomFlip` that had been silently wrong in my paper draft (`RandonFlip`). The use of `lr=` in the Adam optimizer, which was deprecated and removed in TensorFlow 2.11 — meaning my original code wouldn't even run on a current install without changes.

Beyond bug fixes, Claude rebuilt the architecture with three improvements:

**BatchNormalization** was added after each Conv2D block. My original relied on Dropout alone for regularization. BatchNorm stabilizes the values flowing between layers and speeds up training.

**EarlyStopping** replaced my manual epoch tuning. In 2020 I just tried different epoch counts and watched what happened. The new script monitors validation loss and stops automatically when it stops improving, with the best weights restored. The guesswork is gone.

**A confusion matrix** was added alongside the accuracy graphs. A false negative (missed obstacle) is catastrophic in a real self-driving car. A false positive (phantom obstacle) is annoying. The confusion matrix separates them and gives you recall, which is the metric that actually maps to the safety argument in my paper.

### The dataset

My 200-image dataset was the weakest part of the original project, and I knew it. My experience with automation is much better now than it was in college, I cannot imagine myself manually doing any image scraping now. I knew I could automate the gathering of images I needed, I just needed to figure out how.

Claude recommended BDD100K — a Berkeley research dataset of 100,000 dashcam images with JSON annotations tagging every image by time of day, weather, and object category.Then Claude wrote a complete filtering script that parsed those annotations and automatically selected and sorted images into the right folder structure. Instead of spending an afternoon manually sorting screenshots, I ran one command. The new dataset is 2,000 images — 10x the original — drawn from a citable academic source.

The script also logged a condition breakdown of the unbiased pool: what fraction of images were daytime vs. night vs. dusk/dawn. That kind of methodological transparency is what separates a rigorous experiment from a casual one.

---

## What the comparison actually shows

The surface-level story is: AI tools made the work faster. That's true but not that interesting.

The deeper story is about what kind of work gets done when a tool helps transform my ideas into reality-in a timely manner.

In 2020, most of my time went to *logistics* — finding images, reading documentation, debugging cryptic TensorFlow errors, formatting code. I had lots of "busy" work. The thinking about the actual experiment — what exactly constitutes a "biased" dataset, what metrics would make the argument most convincing, how to structure the four experimental conditions so the results were interpretable — got squeezed into whatever time was left.

In 2026, the logistics were handled in minutes. That meant I could spend time on the things that actually mattered: the experimental design, the metric choices, the story the results would tell.

---

## What stayed the same

The experiment. The core question — does biased training data degrade obstacle detection in conditions the model hasn't seen? — is the same question I asked in 2020.

The code structure is also largely the same. The 2020 version wasn't wrong, it was just incomplete and slightly broken.

And the thing that felt true in 2020 — that you can learn a lot by building something modest and watching where it fails — still feels true. The value of the original project wasn't the accuracy numbers. It was that I built something from scratch and understood, at least partially, why it worked. The 2026 version just gave me more of that understanding, faster.

---

## Next Steps

Now that I have a plan and the tools to make it happen, I will need to run the experiments. I will download BDD100K, run the scripts locally, upload the datasets to Kaggle, and actually train the model. More to come on the results in a future blog post.

---

## Tools used

- **Claude Sonnet 4.6** for architecture review, code modernization, dataset design, and explanation
- **TensorFlow 2.x / Keras** for the CNN
- **BDD100K** (Berkeley DeepDrive) for the image dataset
- **Kaggle** for cloud training
- **Python / PIL / scikit-learn** for data processing and evaluation

-Olivia

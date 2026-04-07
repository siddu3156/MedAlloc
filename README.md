# MedAlloc: RL-Based Hospital Resource Allocation Environment

## Problem Description

MedAlloc simulates a hospital emergency system where an AI agent allocates doctors to patients based on urgency and resource availability.

## Environment Overview

The environment follows OpenEnv API:

* reset()
* step(action)
* state()

## State Space

The state includes:

* number of patients
* number of doctors

Example:
{
"patients": 5,
"doctors": 2
}

## Action Space

Agent actions:

* assign doctor
* delay patient

## Reward Function

* positive reward for correct treatment
* negative reward for delays
* score range: 0.0 to 1.0

## Tasks

* Easy: low load
* Medium: moderate load
* Hard: high load

## Grading

Evaluation based on:

* efficiency
* resource usage
* completion

## API Endpoints

* /reset
* /step
* /state

## Setup Instructions

Run locally:
pip install fastapi uvicorn numpy
python inference.py --all

Run API:
uvicorn app:app --host 0.0.0.0 --port 7860

## Deployment

Docker-based deployment on Hugging Face Spaces.

# Intent.md — Optional PRD Draft (Build 1)

Use this as a scratchpad if helpful. Publish the required PRD and Build 1 log on `docs/index.html`; this file is not a separate hand-in.

**Build 1 due:** Monday, Nov 9, 2026 at noon, New York time  
**Builder:** Asha

---

## 1. Who is it for?
*Name a specific person or role you have direct access to (not a broad demographic). Who will actually test and use this before Demo Day?*

- **Target user:** Me, as the person who usually organizes group trips with friends.
- **How I will reach them to test it:** Through our group chat.

## 2. What job does it do?
*Describe the concrete recurring problem from work, school, or life, and what "done" looks like for the user.*

- **Current painful workflow (before):**
  1. Someone proposes a trip in the group chat.
  2. The organizer researches stays, restaurants, and activities across Airbnb, Google, TikTok, and blogs.
  3. Links get dumped in the chat; most get buried or ignored.
  4. People reply slowly or vaguely ("I'm down for anything").
  5. The organizer guesses what people want, builds the plan alone, and chases everyone about money and bookings.

  **Pain:** One person does all the work, decisions stall, and the final plan rarely reflects what everyone wanted.
- **New workflow with this product (after):**
  1. The organizer enters destination, dates, group size, budget, and vibe, and pastes links to a few Airbnb or VRBO options the group is considering.
  2. Each friend opens the trip link and fills out a quick profile: budget comfort, food preferences and restrictions, activity interests, energy level, and dealbreakers. Fernweh combines everyone's profiles to understand the group.
  3. Fernweh suggests restaurants and activities that fit the whole group, so nobody has to research or paste links for those. Friends can optionally add a spot they already know about.
  4. Everyone swipes right or left on restaurants and activities; stays get a comparison view with key details, links, and cost per person.
  5. Fernweh shows group matches and builds 2–3 itinerary options from them (for example, relaxed, packed, and budget-friendly), each with cost per person. The group votes on a final plan, and Fernweh creates a booking plan with what to book and when.
- **Why this is useful** *(used weekly / saves real time / worth paying for)*: Replaces one person doing all the planning alone with a process where everyone's preferences actually shape the trip, and decisions stop stalling.

## 3. What is in and out of scope?

- **One core workflow:** Trip setup, per-friend profiles via the trip link, AI-suggested restaurant and activity options, group swiping, and a results view with matches.
*You have six weeks. List the features, integrations, and polish you are deliberately NOT building.*

- [ ] Not building: Booking or paying for anything inside the app.
- [ ] Not building: Direct connections to Airbnb, VRBO, OpenTable, or Resy — stays are added as pasted links.
- [ ] Not building: User accounts and profiles saved across trips — each friend fills out a quick profile per trip through the shared link.
- **Later / stretch (beyond Build 1 core scope):** Stays comparison with cost per person, 2–3 itinerary options with a group vote, travel-agent features (reservation prep, booking timeline), reusable profiles across trips, destination comparison.

## 4. Rough Local Prototype
*What did you spike this week to test the core idea, and what did you learn from throwing it at the problem?*

- **Local run command / branch / screenshot:** `python3 trip_prototype.py` · see `docs/fernweh-prototype.png`
- **What worked vs. what surprised me:** What worked: each suggestion explains which friends it fits, with a cost per person. What surprised me: some repetition (two fado options), and suggestions need verification since they're AI-generated.

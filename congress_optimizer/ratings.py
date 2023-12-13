"""Functions related to ratings."""

import json

from congress_optimizer.config import RATINGS_DIR
from congress_optimizer.models import Event, Rating


def load_ratings() -> list[Rating]:
    # create ratings directory if it doesn't exist
    RATINGS_DIR.mkdir(parents=True, exist_ok=True)

    # load ratings
    ratings_files = list(RATINGS_DIR.glob("*.json"))
    ratings = [
        Rating(**json.loads(open(rating_file).read())) for rating_file in ratings_files
    ]
    return ratings


def filter_unrated_events(
    events: list[Event],
    ratings: list[Rating],
) -> list[Event]:
    """
    Filters the unrated events from a list of events based on previous ratings.

    Args:
        events: list of events.
        previous_ratings: list of previous ratings.
    Returns:
        List of events for which no rating is provided.
    """
    rated_event_ids = [rating.event_id for rating in ratings]
    unrated_events = [event for event in events if event.id not in rated_event_ids]
    return unrated_events


def enquire_and_save_ratings(events: list[Event]) -> None:
    """Enquire and save ratings for a list of events."""

    for i, event in enumerate(events):
        print(f"\nEvent ({i + 1}/{len(events)}):\n  {event}")
        try:
            score = input("Rate from 0 to 10 (Enter to exit): ")
            if score == "":
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        rating = Rating(event_id=event.id, score=float(score))

        # save rating
        with open(RATINGS_DIR / f"rating_{event.id}.json", "w") as f:
            print(f"Saving rating '{rating.score}' for event '{event.name}'...")
            f.write(rating.model_dump_json())

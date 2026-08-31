#!/usr/bin/env python3
"""Small check for the privileged grasp-following rule."""

from grasp_verification import evaluate_grasp_following


def snapshot(position):
    return {"objects": {"black_bowl": {"position": position}}}


if __name__ == "__main__":
    held = evaluate_grasp_following(
        snapshot([0, 0, 0]), snapshot([0.03, 0, 0]), "black_bowl",
        [0, 0, 0.1], [0.03, 0, 0.1], 0.02, 0.01, 0.015,
    )
    empty = evaluate_grasp_following(
        snapshot([0, 0, 0]), snapshot([0, 0, 0]), "black_bowl",
        [0, 0, 0.1], [0.03, 0, 0.1], 0.02, 0.01, 0.015,
    )
    assert held["verified"]
    assert not empty["verified"]
    print("grasp verification rule: OK")

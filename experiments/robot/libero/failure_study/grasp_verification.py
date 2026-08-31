"""Privileged simulator-only grasp verification helpers."""

import numpy as np


def nearest_named_object(snapshot, point, name_fragment="bowl"):
    """Return the matching object nearest to an end-effector position."""
    point = np.asarray(point, dtype=float)
    candidates = {
        name: float(np.linalg.norm(np.asarray(state["position"], dtype=float) - point))
        for name, state in snapshot.get("objects", {}).items()
        if name_fragment.lower() in name.lower()
    }
    return min(candidates, key=candidates.get) if candidates else None


def evaluate_grasp_following(
    start_snapshot,
    current_snapshot,
    target_name,
    eef_start,
    eef_current,
    min_eef_motion,
    min_target_motion,
    max_relative_drift,
):
    """Return following metrics after sufficient gripper motion, otherwise None."""
    start_target = start_snapshot.get("objects", {}).get(target_name)
    current_target = current_snapshot.get("objects", {}).get(target_name)
    if start_target is None or current_target is None:
        return None

    eef_start = np.asarray(eef_start, dtype=float)
    eef_current = np.asarray(eef_current, dtype=float)
    target_start = np.asarray(start_target["position"], dtype=float)
    target_current = np.asarray(current_target["position"], dtype=float)
    eef_motion = float(np.linalg.norm(eef_current - eef_start))
    if eef_motion < min_eef_motion:
        return None

    target_motion = float(np.linalg.norm(target_current - target_start))
    relative_drift = float(np.linalg.norm((target_current - eef_current) - (target_start - eef_start)))
    return {
        "verified": target_motion >= min_target_motion and relative_drift <= max_relative_drift,
        "eef_motion_m": eef_motion,
        "target_motion_m": target_motion,
        "relative_drift_m": relative_drift,
    }

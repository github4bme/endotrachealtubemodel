from IntegrationClasses import *

def test_evaluating_to_aiming():
    state = EvaluatingAnatomyState()
    state = state.Execute(0)
    assert isinstance(state, AimingState)

def test_aiming_to_moving():
    state = AimingState()
    state = state.Execute(0)
    assert isinstance(state, MovingState)

test_evaluating_to_aiming()
test_aiming_to_moving()
print("All tests passed")
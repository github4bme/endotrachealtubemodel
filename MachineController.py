from IntegrationClasses import *
import time


def start_execution():
    state = EvaluatingAnatomyState()

    while (True):
        currentTime = time.time()
        dt = currentTime - lastFrameTime
        lastFrameTime = currentTime

        state = state.Execute(dt)

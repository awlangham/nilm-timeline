export const yPadding = 0.25;

export const onEventChartMargin = {
    'top': 20,
    'bottom': 35,
    'left': 50,
    'right': 8
};

export const offEventChartMargin = {
    'top': 20,
    'bottom': 35,
    'left': 8,
    'right': 50
};

export const timelineChartMargin = {
    'top': 50,
    'bottom': 75,
    'left': 300,
    'right': 50,
};

export const formatSeconds = (timeInSeconds) => {
    const numMinutes = Math.floor(timeInSeconds / 60);
    const numSeconds = Math.round(timeInSeconds - numMinutes * 60);

    if (numMinutes > 0) {
        return numMinutes + " min., " + numSeconds + " sec."
    } else {
        return numSeconds + " sec."
    }
}
export const yPadding = 0.25;

export const margin = {
    'top': 20,
    'bottom': 75,
    'left': 110,
    'right': 50
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
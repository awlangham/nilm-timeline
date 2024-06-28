import * as d3 from "d3";

const formatMillisecond = d3.timeFormat(".%L"),
    formatSecond = d3.timeFormat(":%S"),
    formatMinute = d3.timeFormat("%H:%M"),
    formatHour = d3.timeFormat("%H:00"),
    formatDay = d3.timeFormat("%a %d"),
    formatWeek = d3.timeFormat("%b %d"),
    formatMonth = d3.timeFormat("%B"),
    formatYear = d3.timeFormat("%Y");

export const multiFormat = (date) => {
    return (
        d3.timeSecond(date) < date
            ? formatMillisecond
            : d3.timeMinute(date) < date
                ? formatSecond
                : d3.timeHour(date) < date
                    ? formatMinute
                    : d3.timeDay(date) < date
                        ? formatHour
                        : d3.timeMonth(date) < date
                            ? d3.timeWeek(date) < date
                                ? formatDay
                                : formatWeek
                            : d3.timeYear(date) < date
                                ? formatMonth
                                : formatYear
    )(date);
};
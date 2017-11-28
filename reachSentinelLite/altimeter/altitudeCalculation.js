var M = 0.0289644;
var g = 9.80665;
var R = 8.31432;
//set these from ground data
var p_default = 101325;
var t_default = 288.15;

//no idea what this does
function noChange(a) {
    return a
}
/*
var unitConversions = {
    F: {
        F: noChange,
        C: function(a) {
            return ((a - 32) * 5) / 9
        },
        K: function(a) {
            return (a - 32) / 1.8 + 273.15
        },
        standard: function(a) {
            return (a - 32) / 1.8 + 273.15
        }
    },
    C: {
        F: function(a) {
            return (a * 1.8) + 32
        },
        C: noChange,
        K: function(a) {
            return a + 273.15
        },
        standard: function(a) {
            return a + 273.15
        }
    },
    K: {
        F: function(a) {
            return (a * 1.8) - 459.67
        },
        C: function(a) {
            return a - 273.15
        },
        K: noChange,
        standard: noChange
    },
    ft: {
        m: function(a) {
            return a * 0.3048
        },
        ft: noChange,
        standard: function(a) {
            return a * 0.3048
        }
    },
    m: {
        m: noChange,
        ft: function(a) {
            return a * 3.2808
        },
        standard: noChange
    },
    Pa: {
        Pa: noChange,
        psi: function(a) {
            return a / 6894.75729
        },
        atm: function(a) {
            return a / 101325
        },
        standard: noChange
    },
    psi: {
        Pa: function(a) {
            return a * 6894.75729
        },
        psi: noChange,
        atm: function(a) {
            return a / 14.6959488
        },
        standard: function(a) {
            return a * 6894.75729
        }
    },
    atm: {
        Pa: function(a) {
            return a * 101325
        },
        psi: function(a) {
            return a * 14.6959488
        },
        atm: noChange,
        standard: function(a) {
            return a * 101325
        }
    }
};

function convertUnits(a, c, b) {
    b = b == null ? "standard" : b;
    return unitConversions[c][b](a)
}
*/

function altcalc(a, k, i) {
    if ((a / i) < (101325 / 22632.1)) {
        var d = -0.0065;
        var e = 0;
        var j = Math.pow((i / a), (R * d) / (g * M));
        return e + ((k * ((1 / j) - 1)) / d)
    } else {
        if ((a / i) < (101325 / 5474.89)) {
            var e = 11000;
            var b = k - 71.5;
            var f = (R * b * (Math.log(i / a))) / ((-g) * M);
            var l = 101325;
            var c = 22632.1;
            var h = ((R * b * (Math.log(l / c))) / ((-g) * M)) + e;
            return h + f
        }
    }
    return NaN
}

function press_temp_alt(b, k, j) {
    if (j < 11000) {
        var e = -0.0065;
        var i = 0;
        return b * Math.pow(k / (k + (e * (j - i))), (g * M) / (R * e))
    } else {
        if (j <= 20000) {
            var e = -0.0065;
            var i = 0;
            var f = 11000;
            var a = b * Math.pow(k / (k + (e * (f - i))), (g * M) / (R * e));
            var c = k + (11000 * (-0.0065));
            var d = 0;
            return a * Math.exp(((-g) * M * (j - f)) / (R * c))
        }
    }
    return NaN
}

function getUnits(a) {
    return $(a).find("select.units").first().val()
}

function getInput(c, a) {
    var b = parseFloat($(c).find("input").first().val());
    if (a == true) {
        return b
    }
    return convertUnits(b, getUnits(c))
}

function setInput(d, c, a) {
    var b = c;
    if (a != null) {
        b = convertUnits(c, a, getUnits(d))
    }
    b = b.toFixed(2);
    if (isNaN(b)) {
        b = ""
    }
    $(d).find("input").first().val(b);
    return b
}

function computePressure() {
    var b = getUnits("#pressure2");
    var e = getInput("#sealevel2");
    var a = getInput("#temperature2");
    var d = getInput("#altitude2");
    if (d > 20000) {
        alert("The maximum altitude is 20,000 meters (65,617 feet).");
        return
    }
    var c = press_temp_alt(e, a, d);
    setInput("#pressure2", c, "Pa")
}

function computeAltitude() {
    var d = getInput("#sealevel1");
    var a = getInput("#temperature1");
    var c = getInput("#pressure1");
    if ((d / c) >= (101325 / 5474.89)) {
        alert("The calculated altitude exceeds the maximum of 20,000 meters (65,617 feet).");
        return
    }
    var b = altcalc(d, a, c);
    setInput("#altitude1", b, "m")
}

function changeUnits(a) {
    var b = "#" + $(this).parent().attr("id");
    setInput(b, getInput(b, true), fieldUnits[b]);
    fieldUnits[b] = getUnits(b)
}
var fieldUnits = {};
$(document).ready(function() {
    $("div.input").each(function(a, b) {
        fieldUnits["#" + b.id] = $(b).find("select.units").first().val()
    });
    $("select.units").change(changeUnits);
    $("#computePress").click(computePressure);
    $("#computeAlt").click(computeAltitude);
    $("span.sealevel.default").click(function() {
        setInput("#" + $(this).parent().attr("id"), p_default, "Pa")
    });
    $("span.temperature.default").click(function() {
        setInput("#" + $(this).parent().attr("id"), t_default, "K")
    })
});
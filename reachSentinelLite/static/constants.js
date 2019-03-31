// -------- TIME UNIT STANDARDIZATION --------

const SECS = 1000;     // 1000 milliseconds
const MINS = 60*SECS;  // 60 seconds
const HOURS = 60*MINS; // 60 minutes

// -------- PACKET ORDERING --------

var TIMESTAMP = 0;
var ACCEL_X = 1;
var ACCEL_Y = 2;
var ACCEL_Z = 3;
var GYRO_X = 4;
var GYRO_Y = 5;
var GYRO_Z = 6;
var MAG_X;
var MAG_Y;
var MAG_Z;
var MAGHEAD;
var ALTITUDE;
var BARO = 7;
var TEMP = 8;

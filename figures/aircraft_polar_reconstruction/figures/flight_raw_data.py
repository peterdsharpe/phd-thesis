from common import *

fig, ax = plt.subplots(figsize=(6.5, 4.5))

speed_color = "darkgreen"
alt_color = "navy"
voltage_color = "red"
current_color = "darkgoldenrod"




plt.plot(
    *simple_read("airspeed"),
    color=speed_color, alpha=0.5,
    label="Airspeed [m/s]"
)
baro_data = simple_read("baro_alt")
baro_altitude_at_takeoff = baro_data[1][0]
plt.plot(
    baro_data[0], baro_data[1] - baro_altitude_at_takeoff,
    color=alt_color, alpha=0.5,
    label="Altitude AGL (from barometer) [m]"
)
plt.plot(
    *simple_read("voltage"),
    color=voltage_color, alpha=0.5,
    label="Battery Voltage [V]"
)
plt.plot(
    *simple_read("current"),
    color=current_color, alpha=0.5,
    label="Battery Current [A]"
)

plt.xlabel("Time after Takeoff [seconds]")
plt.ylabel("Value (see legend)")
# plt.title("Raw Sensor Data")
p.set_ticks(20, 5, 5, 1)
plt.xlim(-1, t_max + 1)
plt.ylim(bottom=-2)
plt.legend(ncols=2)
p.show_plot(
    savefig="flight_raw_data.pdf",
    legend=False
)
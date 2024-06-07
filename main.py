from robot.interface import step, SOUTH, EAST, paint, load_field

load_field("field")

step(SOUTH)
step(EAST)
paint()
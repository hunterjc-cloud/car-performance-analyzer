from drafter import *
from dataclasses import dataclass

#Website information
set_website_title("Car Performance Analyzer")
set_site_information(
    author="Hunter",
    description="Enter vehicle specifications, calculate performance metrics, and compare different cars.",
    sources="Thanks to the Drafter documentation, Python documentation, and my course materials.",
    planning=["planned out on paper and in google docs"],
    links=["https://github.com/hunterjc-cloud/car-performance-analyzer"]
)
hide_debug_information()
set_website_framed(False)

# Stores information about each car
@dataclass
class Car:
    make: str
    model: str
    year: int
    mass: float
    horsepower: float
    top_speed: float


# Stores information for the entire website
@dataclass
class State:
    cars: list[Car]
    selected_car: str
    calculation_result: str
    comparison_result: str
    calculation_history: list[str]
    status: str


# Navigation links used on each page
def navigation():
    return [
        Link("Home", "index"), " | ",
        Link("Add Car", "add_car_page"), " | ",
        Link("Garage", "garage"), " | ",
        Link("Calculator", "calculator"), " | ",
        Link("Compare", "compare_page"), " | ",
        Link("History", "history"),
        "\n"
    ]


# HOME PAGE
@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Car Performance Analyzer"),
        "Welcome to the Car Performance Analyzer!",
        "\nEnter cars, calculate performance, and compare vehicles.",
        "\n"
    ] + navigation() + [
        Header("Main Menu"),
        Button("Add a Car", "add_car_page"),
        Button("View Garage", "garage"),
        Button("Performance Calculator", "calculator"),
        Button("Compare Cars", "compare_page"),
        Button("Performance History", "history"),
        "\n",
        state.status
    ])


# ADD CAR PAGE
@route
def add_car_page(state: State) -> Page:
    return Page(state, navigation() + [
        Header("Add a Car"),
        "Enter the vehicle information below.",
        "\nMake:",
        TextBox("make"),
        "\nModel:",
        TextBox("model"),
        "\nYear:",
        TextBox("year"),
        "\nMass (kg):",
        TextBox("mass"),
        "\nHorsepower:",
        TextBox("horsepower"),
        "\nTop Speed (mph):",
        TextBox("top_speed"),
        "\n",
        Button("Save Car", "add_car"),
        "\n",
        state.status
    ])


# SAVE CAR ROUTE
@route
def add_car(state: State, make: str, model: str,
            year: int, mass: float, horsepower: float,
            top_speed: float) -> Page:

    # Check that the numbers are valid
    if year <= 0 or mass <= 0 or horsepower < 0 or top_speed < 0:
        state.status = "Please enter valid vehicle information."
        return add_car_page(state)

    # Create a new car and add it to the list
    new_car = Car(make, model, year, mass, horsepower, top_speed)
    state.cars.append(new_car)

    state.status = "Car successfully added!"
    return garage(state)


# GARAGE PAGE
@route
def garage(state: State) -> Page:
    content = navigation() + [
        Header("Your Car Garage")
    ]

    # Check if there are any cars
    if len(state.cars) == 0:
        content.append("Your garage is empty. Add a car first.")

    else:
        # Display every car in the garage
        for car in state.cars:
            content.append(
                car.make + " " + car.model +
                " (" + str(car.year) + ")"
            )
            content.append(
                "Mass: " + str(car.mass) + " kg"
            )
            content.append(
                "Horsepower: " + str(car.horsepower)
            )
            content.append(
                "Top Speed: " + str(car.top_speed) + " mph"
            )
            content.append("\n")

    content.append(Button("Add Another Car", "add_car_page"))

    return Page(state, content)


# CALCULATOR PAGE
@route
def calculator(state: State) -> Page:
    content = navigation() + [
        Header("Performance Calculator")
    ]

    if len(state.cars) == 0:
        content.append("Please add a car before using the calculator.")

    else:
        # Create a list of car names for the SelectBox
        car_names = []
        for car in state.cars:
            car_names.append(
                car.make + " " + car.model + " (" + str(car.year) + ")"
            )

        content.append("Select a car:")
        content.append(SelectBox("selected_car", car_names))

        content.append("\nChoose a calculation:")
        content.append(SelectBox("calculation_type", [
            "Acceleration",
            "Kinetic Energy",
            "Braking Distance"
        ]))

        content.append("\nApplied Force (N):")
        content.append(TextBox("applied_force", 4000))

        content.append("\nDeceleration (m/s^2):")
        content.append(TextBox("deceleration", 8.0))

        content.append("\n")
        content.append(Button("Calculate", "calculate_performance"))

    content.append("\nLatest Result:")
    content.append(state.calculation_result)

    return Page(state, content)


# PERFORM CALCULATIONS
@route
def calculate_performance(state: State, selected_car: str,
                           calculation_type: str,
                           applied_force: float,
                           deceleration: float) -> Page:

    state.selected_car = selected_car

    # Find the selected car
    selected_vehicle = None

    for car in state.cars:
        car_name = car.make + " " + car.model + " (" + str(car.year) + ")"

        if car_name == selected_car:
            selected_vehicle = car

    if selected_vehicle is None:
        state.status = "Please select a valid car."

    elif calculation_type == "Acceleration":
        acceleration = applied_force / selected_vehicle.mass

        state.calculation_result = (
            "Acceleration: " + str(round(acceleration, 2)) + " m/s^2"
        )

    elif calculation_type == "Kinetic Energy":
        speed = selected_vehicle.top_speed * 0.44704
        energy = 0.5 * selected_vehicle.mass * speed ** 2

        state.calculation_result = (
            "Kinetic Energy: " + str(round(energy, 2)) + " Joules"
        )

    elif calculation_type == "Braking Distance":
        speed = selected_vehicle.top_speed * 0.44704

        if deceleration <= 0:
            state.calculation_result = "Enter a positive deceleration."

        else:
            distance = speed ** 2 / (2 * deceleration)

            state.calculation_result = (
                "Braking Distance: " + str(round(distance, 2)) + " meters"
            )

    # Save the calculation in history
    state.calculation_history.append(state.calculation_result)

    state.status = "Calculation completed!"

    return calculator(state)


# COMPARE CARS PAGE
@route
def compare_page(state: State) -> Page:
    content = navigation() + [
        Header("Compare Cars")
    ]

    if len(state.cars) < 2:
        content.append("You need at least two cars to compare.")

    else:
        car_names = []

        for car in state.cars:
            car_names.append(
                car.make + " " + car.model + " (" + str(car.year) + ")"
            )

        content.append("Choose the first car:")
        content.append(SelectBox("car_one", car_names))

        content.append("\nChoose the second car:")
        content.append(SelectBox("car_two", car_names))

        content.append("\n")
        content.append(Button("Compare Cars", "compare_cars"))

    content.append("\nComparison Result:")
    content.append(state.comparison_result)

    return Page(state, content)


# COMPARE TWO CARS
@route
def compare_cars(state: State, car_one: str, car_two: str) -> Page:

    first_car = None
    second_car = None

    # Find both cars
    for car in state.cars:
        car_name = car.make + " " + car.model + " (" + str(car.year) + ")"

        if car_name == car_one:
            first_car = car

        if car_name == car_two:
            second_car = car

    if first_car is None or second_car is None:
        state.comparison_result = "Please select two valid cars."

    elif car_one == car_two:
        state.comparison_result = "Please select two different cars."

    else:
        # Calculate horsepower per metric ton
        ratio_one = first_car.horsepower / (first_car.mass / 1000)
        ratio_two = second_car.horsepower / (second_car.mass / 1000)

        if ratio_one > ratio_two:
            state.comparison_result = car_one + " has the better horsepower-to-weight ratio."

        elif ratio_two > ratio_one:
            state.comparison_result = car_two + " has the better horsepower-to-weight ratio."

        else:
            state.comparison_result = "Both cars have the same ratio."

    return compare_page(state)


# HISTORY PAGE
@route
def history(state: State) -> Page:
    content = navigation() + [
        Header("Performance History")
    ]

    if len(state.calculation_history) == 0:
        content.append("No calculations have been completed yet.")

    else:
        # Display previous calculations
        for result in state.calculation_history:
            content.append(result)
            content.append("\n")

    return Page(state, content)


# START THE WEBSITE
start_server(State(
    [],
    "",
    "",
    "",
    [],
    "Welcome! Add a car to get started."
))


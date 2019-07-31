import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.fetchToday();
    this.fetchAvailability();
    this.fetchBookedTimes();
  }

  async fetchToday() {
    try {
      const res = await fetch("http://localhost:4433/today");
      const json = await res.json();
      this.setState({today: json.today});
    } catch (e) {
      console.error("Failed to fetch 'today' data", e);
    }
  }

  async fetchAvailability() {
    try {
      const res = await fetch("http://localhost:4433/availability");
      const json = await res.json();
      this.setState({availability: json.availability});
    } catch (e) {
      console.error("Failed to fetch availability data", e);
    }
  }

  async fetchBookedTimes() {
    try {
      const res = await fetch("http://localhost:4433/booked");
      const json = await res.json();
      this.setState({booked: json.booked});
    } catch (e) {
      console.error("Failed to fetch reserved data", e);
    }
  }

  handleClick = (advisor_id, chosen_time) => {
    console.log("button clicked");
    if (this.state.name) {
      this.setState({formerror: null})
      const data = {
        "student_name": this.state.name,
        "advisor_id": advisor_id,
        "chosen_time": chosen_time
      }
      fetch("http://localhost:4433/selected",
        {
          headers: {
            'Content-Type': 'application/json'
          },
          method: 'POST',
          body: JSON.stringify(data)
        }
      )
      .then(() => {
        this.fetchBookedTimes()
        this.fetchAvailability();
      });
    } else {
      this.setState({formerror: 'Please enter a name to book a time.'})
      window.scrollTo(0, 0);
    }
  }

  render() {

    return (
      <div className="App container">
        <h1>Book Time with an Advisor</h1>
        <div>
          {this.state.today && <span id="today">Today is {this.state.today}.</span>}
        </div>
        <div>
          {this.state.formerror &&
          <p className="alert alert-danger">{this.state.formerror}</p>}
        </div>
        <form id="name-form" className="col-md-6">
          <div className="form-group">
            <label htmlFor="name-field">Your Name</label>
            <input type="text" id="name-field" className="form-control"
              onChange={ev => this.setState({name: ev.target.value})}/>
          </div>
        </form>


        <h2>Available Times</h2>
        <table className="advisors table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Available Times</th>
            </tr>
          </thead>
          {this.state.availability &&
            <tbody>
            {this.state.availability.map((advisor, key) => {
              return (
                <tr key={advisor.id}>
                  <td>{advisor.id}</td>
                  <td>
                    <ul className="list-unstyled">
                      {advisor.open_times.map((open_time, index) => {
                        return <li>
                          <time dateTime={open_time}
                            className="book-time">{open_time}</time>
                          <button className="book btn-small btn-primary"
                            onClick={this.handleClick.bind(this, advisor.id, open_time)}>
                            Book
                          </button>
                        </li>
                      })}
                    </ul>
                  </td>
                </tr>
              )
              })
            }
            </tbody>
          }
        </table>


        <h2>Booked Times</h2>
        <table className="bookings table">
          <thead>
            <tr>
              <th>Advisor ID</th>
              <th>Student Name</th>
              <th>Date/Time</th>
            </tr>
          </thead>
          {this.state.booked &&
            <tbody>
            {this.state.booked.map((booked, key) => {
              return (
                <tr key={booked.chosen_time}>
                  <td>{booked.advisor_id}</td>
                  <td>{booked.student_name}</td>
                  <td>{booked.chosen_time}</td>
                </tr>
              )
              })
            }
            </tbody>
          }
        </table>
      </div>
    );
  }
}

export default App;

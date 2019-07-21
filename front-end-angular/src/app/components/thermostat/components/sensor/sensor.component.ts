import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.css']
})
export class SensorComponent implements OnInit {

  @Input() public sensor;

  constructor() { }

  ngOnInit() {
  }

}

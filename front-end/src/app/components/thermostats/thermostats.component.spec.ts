import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ThermostatsComponent } from './thermostats.component';

describe('ThermostatsComponent', () => {
  let component: ThermostatsComponent;
  let fixture: ComponentFixture<ThermostatsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ThermostatsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ThermostatsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

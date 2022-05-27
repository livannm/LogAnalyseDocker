import { NgModule } from '@angular/core';
import {BrowserModule, HammerModule} from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './Widgets/navbar/navbar.component';
import { VisualisationComponent } from './visualisation/visualisation.component';
import {HttpClient, HttpClientModule} from "@angular/common/http";
import {MatTableModule} from "@angular/material/table";
import {MatPaginatorModule} from "@angular/material/paginator";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {MatSortModule} from "@angular/material/sort";
import { AffluenceComponent } from './affluence/affluence/affluence.component';
import {NgChartsModule} from "ng2-charts";
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MatInputModule } from '@angular/material/input';
import {  } from "@angular/material";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatAutocompleteModule} from "@angular/material/autocomplete";
import 'hammerjs';
import {ScrollingModule} from "@angular/cdk/scrolling";
import { VisualisationSiteqComponent } from './visualisation-siteq/visualisation-siteq.component';
import {MatButtonModule} from "@angular/material/button";
import { CarteWidgetComponent } from './Widgets/carte-widget/carte-widget.component';

import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { RechercheSiteComponent } from './Widgets/recherche-site/recherche-site.component';
import { NavbarDecoComponent } from './navbar-deco/navbar-deco.component';
import { WelcomeComponent } from './welcome/welcome.component';
import { AnalyseIpComponent } from './analyse-ip/analyse-ip.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    VisualisationComponent,
    AffluenceComponent,
    VisualisationSiteqComponent,
    CarteWidgetComponent,
    VisualisationSiteqComponent,
    RegisterComponent,
    LoginComponent,
    VisualisationSiteqComponent,
    RechercheSiteComponent,
    NavbarDecoComponent,
    WelcomeComponent,
    AnalyseIpComponent,

  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        MatTableModule,
        MatPaginatorModule,
        BrowserAnimationsModule,
        MatSortModule,
        NgChartsModule,
        MatFormFieldModule,
        MatSelectModule,
        NgbModule,
        MatInputModule,
        ReactiveFormsModule,
        MatAutocompleteModule,
        HammerModule,
        ScrollingModule,
        MatButtonModule,
        FormsModule,
    ],
  providers: [ ],
  bootstrap: [AppComponent]
})
export class AppModule { }

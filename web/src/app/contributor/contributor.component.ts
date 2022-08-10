import { Component, OnInit } from '@angular/core';
import { ContributorInterface } from '@interface/contributor.interface';

@Component({
  selector: 'app-contributor',
  templateUrl: './contributor.component.html',
  styleUrls: ['./contributor.component.scss']
})
export class ContributorComponent implements OnInit {

  contributors: Array<ContributorInterface> = [
    {
      name: "Zacharie C-L",
      profilePictureUrl: "https://avatars.githubusercontent.com/u/55606963?v=4",
      githubUrl: "https://github.com/Cor-Lapidem",
    },
    {
      name: "Armand Briere",
      profilePictureUrl: "https://avatars.githubusercontent.com/u/46636172?v=4",
      githubUrl: "https://github.com/ArmandBriere",
    },
    {
      name: "Pierre-Marc Dameus",
      profilePictureUrl: "https://avatars.githubusercontent.com/u/22399745?v=4",
      githubUrl: "https://github.com/wildman777",

    }
  ];
  constructor() { }

  ngOnInit(): void {
  }

  openGithubPage(contributor: ContributorInterface): void {
    window.open(contributor.githubUrl, '_blank');
  }

}

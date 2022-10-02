import { Component, OnInit } from '@angular/core';
import { ServerInterface } from '@interface/server.interface';
import { ServerService } from './server.service';

@Component({
  selector: 'app-server',
  templateUrl: './server.component.html',
  styleUrls: ['./server.component.scss']
})
export class ServerComponent implements OnInit {

  servers: ServerInterface[] | undefined;

  constructor(private serverService: ServerService) { }

  ngOnInit(): void {
    this.serverService.getServers().subscribe(data => {
      this.servers = data;
    });
  }

  joinServer(join_url: string): void {
    window.open(join_url, '_blank');
  }
}

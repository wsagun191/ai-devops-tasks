flowchart TD
    Start([Start Builda]) --> Checkout[1. Checkout kodu z Git]
    
    subgraph CI [Continuous Integration - Budowanie i Jakość]
        Checkout --> Build[2. Budowanie aplikacji<br/>npm run build]
        Build --> UnitTests[3. Testy jednostkowe<br/>npm test]
        UnitTests --> StaticAnalysis[4. Analiza statyczna kodu<br/>SonarQube]
        StaticAnalysis --> Security[5. Bezpieczeństwo<br/>Skanowanie podatności / SAST]
    end

    subgraph Containerization [Konteneryzacja]
        Security --> DockerBuild[6. Budowanie obrazu Docker<br/>docker build]
        DockerBuild --> IntegrationTests[7. Testy integracyjne<br/>w kontenerze / E2E]
    end

    subgraph CD [Continuous Deployment - Wdrożenia]
        IntegrationTests --> Staging[8. Wdrożenie na środowisko Staging]
        Staging --> ManualApproval{9. Zatwierdzenie ręczne<br/>i branch production?}
    end

    ManualApproval -->|Tak / Zatwierdzono| Production[10. Wdrożenie na Produkcję]
    ManualApproval -->|Nie / Odrzucono| Abort([Przerwano potok])
    
    Production --> Success([Sukces wdrożenia])

    %% Stylizacja (opcjonalnie dla lepszej czytelności)
    classDef stage fill:#f9f,stroke:#333,stroke-width:2px;
    class Checkout,Build,UnitTests,StaticAnalysis,Security,DockerBuild,IntegrationTests,Staging,Production stage;

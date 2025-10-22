# Product Roadmap Template

Use this template to create a product roadmap organized by theme, outcomes, or phases.

## 12-Month Product Roadmap

### Overview
- **Vision**: [Link to product vision]
- **Planning Horizon**: 12 months (Jan-Dec 20XX)
- **Planning Approach**: [Theme-based / Outcome-based / Risk-based]
- **Key Constraints**: [Budget, team size, market constraints]
- **Success Metrics**: [OKRs and key metrics]

---

## Roadmap by Quarter

### Q1: Foundation & MVP (Jan-Mar)

**Theme:** Product Foundation & MVP Launch

**Goals**
- Launch MVP with core features
- Achieve 40%+ monthly retention
- Validate product-market fit
- Build initial user base (1,000+ beta users)

**Features**

| Feature | Priority | RICE Score | Dependencies | Status |
|---------|----------|-----------|--------------|--------|
| User Authentication | P0 | 1,500 | None | Design |
| Dashboard | P0 | 1,400 | Auth | Design |
| Basic Recommendations | P0 | 1,200 | Analytics | Spec |
| Data Integration (5 banks) | P1 | 900 | Backend API | Spec |
| Goals Tracking | P1 | 700 | Dashboard | Backlog |
| Monthly Reports (PDF) | P2 | 300 | Recommendations | Backlog |

**Outcomes**
- [ ] MVP launched with 3 core features
- [ ] 1,000+ beta users onboarded
- [ ] 40%+ 30-day retention achieved
- [ ] NPS > 30 from beta users
- [ ] Zero critical security issues

**Resources**
- Engineering: 2 FTE
- Design: 1 FTE
- Product: 1 FTE

---

### Q2: User Retention & Expansion (Apr-Jun)

**Theme:** Engagement & Growth

**Goals**
- Improve monthly retention to 55%
- Expand integrations to 20 financial institutions
- Launch premium tier
- Grow user base to 10,000

**Features**

| Feature | Priority | RICE Score | Dependencies | Status |
|---------|----------|-----------|--------------|--------|
| Bank Integrations (15 more) | P0 | 1,600 | Q1 API | In Progress |
| AI-Powered Recommendations | P0 | 1,550 | Analytics | In Progress |
| Alerts & Notifications | P1 | 1,100 | Recommendations | Design |
| Premium Tier | P1 | 950 | Dashboard | Spec |
| Mobile Web (Responsive) | P1 | 800 | Dashboard | Backlog |
| Family Accounts | P2 | 600 | Auth | Backlog |
| Community Forum | P3 | 200 | Auth | Backlog |

**Outcomes**
- [ ] 55% monthly retention achieved
- [ ] 20 institution integrations live
- [ ] Premium tier generating $50K MRR
- [ ] 10,000+ active users
- [ ] NPS > 40 from users

**Resources**
- Engineering: 3 FTE
- Design: 1.5 FTE
- Product: 1 FTE

---

### Q3: Monetization & Scale (Jul-Sep)

**Theme:** Revenue Growth & Market Expansion

**Goals**
- Launch mobile app
- Enter new geographic market (Canada)
- Improve revenue to $200K MRR
- Expand user base to 50,000

**Features**

| Feature | Priority | RICE Score | Dependencies | Status |
|---------|----------|-----------|--------------|--------|
| Native Mobile App (iOS) | P0 | 1,700 | Mobile API | Design |
| Mobile App (Android) | P0 | 1,650 | Mobile API | Design |
| Advisor Network Integration | P0 | 1,400 | Premium tier | Spec |
| Advanced Analytics Dashboard | P1 | 1,000 | Recommendations | Design |
| International Support (Canada) | P1 | 900 | Compliance | Spec |
| Tax Planning Module | P1 | 850 | Recommendations | Backlog |
| API for Partners | P2 | 600 | Backend API | Backlog |

**Outcomes**
- [ ] iOS app launched, 50K+ downloads
- [ ] Android app in beta (20K beta users)
- [ ] $200K MRR revenue
- [ ] 50,000+ active users
- [ ] Launched in Canada market

**Resources**
- Engineering: 4 FTE
- Design: 2 FTE
- Product: 1.5 FTE

---

### Q4: Market Leadership & Growth (Oct-Dec)

**Theme:** Scale & Market Penetration

**Goals**
- Achieve 70%+ monthly retention
- Reach 100,000+ users
- Generate $500K MRR
- Establish market leadership position

**Features**

| Feature | Priority | RICE Score | Dependencies | Status |
|---------|----------|-----------|--------------|--------|
| Financial Advisor Marketplace | P0 | 1,550 | Advisor network | In Progress |
| Social Features (Share Plans) | P0 | 1,200 | Dashboard | Design |
| AI-Powered Optimization | P0 | 1,150 | Recommendations | In Progress |
| B2B White Label | P1 | 950 | Partnerships | Spec |
| Investment Integration | P1 | 900 | Bank integrations | Spec |
| Content Marketing Platform | P1 | 700 | Auth | Backlog |

**Outcomes**
- [ ] 100,000+ active users
- [ ] 70%+ monthly retention
- [ ] $500K MRR revenue
- [ ] 100K+ downloads for mobile apps
- [ ] NPS > 50 from users
- [ ] Market leadership position established

**Resources**
- Engineering: 5 FTE
- Design: 2.5 FTE
- Product: 2 FTE

---

## Feature Prioritization Matrix

### RICE Scoring Results

**High Priority (Scores > 1,000)**
1. User Authentication - 1,500
2. Dashboard - 1,400
3. Bank Integrations (15) - 1,600
4. AI Recommendations - 1,550
5. Mobile App iOS - 1,700
6. Mobile App Android - 1,650
7. Advisor Marketplace - 1,550
8. Social Features - 1,200

**Medium Priority (Scores 500-1,000)**
- Goals Tracking - 700
- Premium Tier - 950
- Alerts & Notifications - 1,100
- Advanced Analytics - 1,000
- International Support - 900
- Mobile Web - 800
- Tax Planning - 850

**Lower Priority (Scores < 500)**
- Family Accounts - 600
- Community Forum - 200
- API for Partners - 600
- Content Platform - 700

---

## Dependencies & Critical Path

```
Q1:
  User Auth → Dashboard
         ↓
    Core Analytics

Q2:
  Q1 Analytics → Bank Integrations → AI Recommendations
                                  ↓
                            Premium Tier

Q3:
  Q1 Dashboard → Mobile App (iOS)
  Mobile API → Mobile App (Android)
  Premium Tier → Advisor Network

Q4:
  Advisor Network → Advisor Marketplace
  Mobile Apps → Social Features
  Bank Integrations → Investment Integration
```

**Critical Path Items** (cannot be delayed without impacting roadmap):
- Q1: User Auth, Dashboard, Analytics
- Q2: Bank Integrations (enable Q3 expansion)
- Q3: Mobile Apps (launch simultaneously iOS/Android)
- Q4: Advisor Network (revenue driver)

---

## Roadmap Themes

### Theme 1: Product Foundation (Q1)
Focus on core functionality and MVP launch
- User authentication and profiles
- Dashboard and recommendations
- Data integration foundation
- Analytics and tracking

### Theme 2: User Retention (Q2)
Focus on engagement and expansion
- Feature expansion (integrations, alerts)
- Premium tier monetization
- Mobile web support
- Community building

### Theme 3: Mobile & Scale (Q3)
Focus on mobile adoption and new markets
- Native mobile applications
- Geographic expansion
- Advisor network
- Advanced analytics

### Theme 4: Market Leadership (Q4)
Focus on differentiation and revenue
- Unique advisor marketplace
- Social and sharing features
- AI optimization
- Partnership opportunities

---

## Roadmap Communication

### For Investors
> "Our roadmap balances innovation with execution. Q1 establishes product-market fit foundation. Q2-Q3 scales to 100K users and $500K MRR through mobile and monetization. Q4 establishes market leadership with unique advisor network and AI optimization."

### For Employees
> "Our 12-month roadmap takes us from MVP to market leadership. Q1 launches the core product, Q2 proves the business model works, Q3 reaches scale, and Q4 establishes us as the category leader."

### For Customers
> "We're building the financial planning platform from your feedback. Q1 launches core features, Q2 adds mobile and premium options, Q3 brings you native apps, and Q4 introduces financial advisor connections."

---

## Roadmap Review Checklist

- [ ] Roadmap aligns with product vision and strategic goals
- [ ] Features are RICE scored with clear business justification
- [ ] Dependencies identified and critical path documented
- [ ] Resource requirements realistic and achievable
- [ ] Quarterly goals specific and measurable
- [ ] Market opportunities addressed (competitive response)
- [ ] Technical debt accounted for (20-30% of capacity)
- [ ] Risk mitigation planned for critical items
- [ ] Stakeholder input incorporated
- [ ] Roadmap flexible enough to adapt to learnings
- [ ] Success metrics defined for each phase
- [ ] Team capacity and dependencies communicated

---

## Regular Roadmap Updates

**Monthly Review**
- Progress against current quarter goals
- Feature status updates
- Blocker identification and resolution
- Metric tracking and learnings

**Quarterly Review**
- Outcome assessment (achieved vs planned)
- Learning incorporation into next quarter
- RICE re-scoring of features
- Roadmap adjustments based on market conditions

**Annual Review**
- Year-end results vs goals
- 3-year strategic plan update
- Next 12-month roadmap creation
- Organizational goal alignment

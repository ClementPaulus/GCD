// Operator session state management
export type OperatorSession = {
  activeContract?: string;
  activeClosures?: string[];
  activeCasepack?: string;
  ledgerState?: any;
  stance?: string;
  memory?: Record<string, any>;
};

export function createOperatorSession(): OperatorSession {
  return {};
}

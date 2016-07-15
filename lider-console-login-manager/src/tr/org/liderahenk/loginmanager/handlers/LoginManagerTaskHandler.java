package tr.org.liderahenk.loginmanager.handlers;

import java.util.Set;

import org.eclipse.swt.widgets.Display;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import tr.org.liderahenk.liderconsole.core.handlers.MultipleSelectionHandler;
import tr.org.liderahenk.loginmanager.dialogs.LoginManagerTaskDialog;

//TODO use MultipleSelectionHandler if this task support multiple LDAP entries/DNs otherwise use SingleSelectionHandler.
public class LoginManagerTaskHandler extends MultipleSelectionHandler {
	
	private Logger logger = LoggerFactory.getLogger(LoginManagerTaskHandler.class);
	
	@Override
	public void executeWithDNSet(Set<String> dnSet) {
		// TODO dnSet contains distinguished names (DN) of the selected LDAP entries.
		LoginManagerTaskDialog dialog = new LoginManagerTaskDialog(Display.getDefault().getActiveShell(), dnSet);
		dialog.create();
		dialog.open();
	}
	
}

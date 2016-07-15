package tr.org.liderahenk.loginmanager.dialogs;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.DateTime;
import org.eclipse.swt.widgets.Label;

import tr.org.liderahenk.liderconsole.core.dialogs.IProfileDialog;
import tr.org.liderahenk.liderconsole.core.exceptions.ValidationException;
import tr.org.liderahenk.liderconsole.core.model.Profile;
import tr.org.liderahenk.loginmanager.constants.LoginManagerConstants;
import tr.org.liderahenk.loginmanager.i18n.Messages;

/**
 * 
 * @author <a href="mailto:mine.dogan@agem.com.tr">Mine Dogan</a>
 *
 */
public class LoginManagerProfileDialog implements IProfileDialog {
	
	private Button btnDays;
	private DateTime startTime;
	private DateTime endTime;
	private DateTime date;
	
	private final String days[] = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"};
	private List<String> chosenDays = new ArrayList<String>();
	
	@Override
	public void init() {
	}
	
	@Override
	public void createDialogArea(Composite parent, Profile profile) {
		Composite composite = new Composite(parent, SWT.NONE);
		composite.setLayout(new GridLayout(1, false));
		
		Label lblDays = new Label(composite, SWT.NONE);
		lblDays.setText(Messages.getString("DAYS"));
		
		Composite compDays = new Composite(composite, SWT.NONE);
		compDays.setLayout(new GridLayout(5, false));
		
		for (int i = 0; i < days.length; i++) {
			String i18n = Messages.getString(days[i]);
			if (i18n != null && !i18n.isEmpty()) {
				btnDays = new Button(compDays, SWT.CHECK);
				btnDays.setData(days[i]);
				btnDays.setText(i18n);
				btnDays.addSelectionListener(new SelectionAdapter() {
					
					@Override
			        public void widgetSelected(SelectionEvent event) {
			            Button btn = (Button) event.getSource();
			            if (btn.getSelection()) {
							chosenDays.add((String) btn.getData());
						}
			        }
				});
			}
	    }
		
		Label lblTimeDate = new Label(composite, SWT.NONE);
		lblTimeDate.setText(Messages.getString("TIME_DATE"));
		
		Composite compOptions = new Composite(composite, SWT.NONE);
		compOptions.setLayout(new GridLayout(2, false));
		
		Label lblStartTime = new Label(compOptions, SWT.NONE);
		lblStartTime.setText(Messages.getString("START_TIME"));
		
		startTime = new DateTime(compOptions, SWT.TIME);
		
		Label lblEndTime = new Label(compOptions, SWT.NONE);
		lblEndTime.setText(Messages.getString("END_TIME"));
		
		endTime = new DateTime(compOptions, SWT.TIME);
		
		Label lblDate = new Label(compOptions, SWT.NONE);
		lblDate.setText(Messages.getString("LAST_AVAILABILITY_DATE"));
		
		date = new DateTime(compOptions, SWT.DATE);
	}
	
	public String convertDateToString(DateTime date) {
		
		int day = date.getDay();
	    int month = date.getMonth() + 1;
	    int year = date.getYear();

	    String strDate = (day < 10) ? "0" + day + "/" : day + "/";
	    strDate += (month < 10) ? "0" + month + "/" : month + "/";
	    strDate += year;
	    
	    return strDate;
	}
	
	public Date convertTimeToDate(DateTime time) {
		
		Calendar calendar = Calendar.getInstance();
		calendar.setTimeInMillis(0); // set to zero epoch
		calendar.set(Calendar.HOUR, time.getHours());
		calendar.set(Calendar.MINUTE, time.getMinutes());
		calendar.set(Calendar.SECOND, time.getSeconds());
		
		return calendar.getTime();
	}
	
	@Override
	public Map<String, Object> getProfileData() throws Exception {
		Map<String, Object> profileData = new HashMap<String, Object>();
		profileData.put(LoginManagerConstants.PARAMETERS.DAYS, chosenDays);
		profileData.put(LoginManagerConstants.PARAMETERS.START_TIME, convertTimeToDate(startTime));
		profileData.put(LoginManagerConstants.PARAMETERS.END_TIME, convertTimeToDate(endTime));
		profileData.put(LoginManagerConstants.PARAMETERS.LAST_DATE, convertDateToString(date));
		return profileData;
	}
	
	@Override
	public void validateBeforeSave() throws ValidationException {
		Date start = convertTimeToDate(startTime);
		Date end = convertTimeToDate(endTime);
		
		if(start.after(end)) {
			throw new ValidationException(Messages.getString("START_TIME_NOT_BIGGER_THAN_END_TIME"));
		}
		
	}
	
}
